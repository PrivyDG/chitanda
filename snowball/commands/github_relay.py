import asyncio
import hashlib
import hmac
import logging
import sys

from aiohttp import web
from discord import Embed

from snowball.config import config
from snowball.listeners import DiscordListener

logger = logging.getLogger(__name__)


def setup(bot):
    if not hasattr(bot, 'webserver_github'):
        bot.webserver_github = _create_webserver(bot)


def _create_webserver(bot):
    app = web.Application()
    app.router.add_route('POST', '/', lambda request, bot=bot, **kwargs: (
        sys.modules[__name__]._handle_request(bot, request, **kwargs)
    ))  # Allow for hot-reloading to change outout.
    try:
        return asyncio.ensure_future(
            asyncio.get_event_loop().create_server(
                app.make_handler(),
                host='0.0.0.0',
                port=int(config['github_relay']['port']),
            )
        )
    except ValueError:
        logging.error('Invalid port value for GitHub webhook webserver.')


async def _handle_request(bot, request, **kwargs):
    events = {
        'push': _handle_push,
        'issues': _handle_issue,
        'pull_request': _handle_pull_request,
    }

    logger.info('Received request from GitHub webhook.')
    if (
        config['github_relay']['secret']
        and not _check_signature(await request.text(), request.headers)
    ):
        logger.info('GitHub request contained invalid signature, ignoring.')
        return web.Response(body='Invalid signature.', status=500)

    payload = await request.json()

    try:
        repo_id = str(payload['repository']['id'])
        cfgs = config['github_relay']['relays'][repo_id]
    except KeyError:
        logger.info('GitHub request\'s repository is not tracked, ignoring.')
        return web.Response(body='Untracked repository.', status=500)
    else:
        logger.info('Event for repository {payload["repository"]["name"]}.')

    try:
        event_handler = events[request.headers['X-Github-Event']]
    except KeyError:
        logger.info('GitHub request\'s event is unsupported, ignoring.')
        return web.Response(body='Unsupported event.', status=500)

    for cfg in cfgs:
        asyncio.ensure_future(
            event_handler(_get_listener(bot, cfg['listener']), payload, cfg)
        )

    return web.Response(body='Received.')


def _check_signature(payload, headers):
    try:
        expected_sig = hmac.new(
            key=config['github_relay']['secret'].encode(),
            msg=payload.encode(),
            digestmod=hashlib.sha1,
        ).hexdigest()
        return hmac.compare_digest(
            f'sha1={expected_sig}',
            headers['X-Hub-Signature'],
        )
    except KeyError:
        pass
    return False


def _get_listener(bot, listener):
    if listener == 'Discord':
        return bot.discord_listener
    elif listener.startswith('IRC@'):
        try:
            return bot.irc_listeners[listener[4:]]
        except KeyError:
            logger.error(f'Invalid IRC listener {listener} for GitHub relay.')
    else:
        logger.error(f'Invalid IRC listener {listener} for GitHub relay.')
    raise KeyError


async def _handle_push(listener, payload, cfg):
    branch = payload['ref'].split('/')[2]

    if payload['ref'].split('/')[1] == 'tags':
        logger.info(f'Received tag push event.')
        return await listener.message(
            target=cfg['channel'],
            message=(
                f'New tag {branch} tracking {payload["before"][:8]} pushed '
                f'to {payload["repository"]["name"]}'
            )
        )

    if cfg['branches'] and branch not in cfg['branches']:
        logger.info(f'Received push event for untracked branch {branch}.')
        return

    def construct_message(payload, branch):
        return (
            f'{_get_num_commits(payload["commits"])} commit(s) pushed to '
            f'{payload["repository"]["name"]}/{branch} by '
            f'{payload["pusher"]["name"]}'
        )

    def construct_commit_message(commit):
        chash = commit['id'][:8]
        url = commit['url'].replace(commit['id'], chash)
        return (
            f'{chash} - {commit["author"]["username"]} - '
            f'{_trim_message(commit["message"])} - {url}'
        )

    logger.info(f'Received push to branch event.')

    if isinstance(listener, DiscordListener):
        embed = Embed(title=construct_message(payload, branch))
        embed.add_field(
            name='Compare',
            value=payload['compare'],
            inline=False,
        )
        for commit in payload['commits']:
            embed.add_field(
                name=(
                    f'{commit["author"]["username"]} - '
                    + commit["url"].replace(commit["id"], commit["id"][:8])
                ),
                value=_trim_message(commit["message"]),
                inline=False,
            )
        await listener.message(
            target=cfg['channel'],
            message=embed,
            embed=True,
        )
    else:
        await listener.message(
            target=cfg['channel'],
            message=construct_message(payload, branch),
        )
        await listener.message(
            target=cfg['channel'],
            message=f'Compare - {payload["compare"]}',
        )
        for commit in payload['commits']:
            await listener.message(
                target=cfg['channel'],
                message=construct_commit_message(commit),
            )


async def _handle_issue(listener, payload, cfg):
    logger.info(f'Received a {payload["action"]} issue event.')
    await listener.message(
        target=cfg['channel'],
        message=(
            f'{payload["sender"]["login"]} {payload["action"]} issue '
            f'{payload["issue"]["number"]} - '
            f'{_trim_message(payload["issue"]["title"], 200)} - '
            f'{payload["issue"]["html_url"]}'
        )
    )


async def _handle_pull_request(listener, payload, cfg):
    logger.info(f'Received a {payload["action"]} pull request event.')
    await listener.message(
        target=cfg['channel'],
        message=(
            f'{payload["sender"]["login"]} {payload["action"]} pull request '
            f'{payload["issue"]["number"]} - '
            f'{_trim_message(payload["issue"]["title"], 200)} - '
            f'{payload["issue"]["html_url"]}'
        )
    )


def _get_num_commits(commits):
    return '20+' if len(commits) == 20 else len(commits)


def _trim_message(message, length=240):
    return f'{message[:length - 3]}...' if len(message) > length else message
