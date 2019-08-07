import re
from asyncio import coroutine
from pathlib import Path

import mock
import pytest
from click.testing import CliRunner

from chitanda import BotError, create_app_dirs
from chitanda.listeners import DiscordListener, IRCListener
from chitanda.util import (
    admin_only,
    allowed_listeners,
    args,
    auth_only,
    channel_only,
    irc_unstyle,
    private_message_only,
    register,
    trim_message,
)


def test_create_app_dirs(monkeypatch):
    with CliRunner().isolated_filesystem():
        config_dir = Path.cwd() / 'config'
        data_dir = Path.cwd() / 'data'
        monkeypatch.setattr('chitanda.CONFIG_DIR', config_dir)
        monkeypatch.setattr('chitanda.DATA_DIR', data_dir)

        create_app_dirs()

        assert config_dir.is_dir()
        assert data_dir.is_dir()


def test_irc_unstyle():
    assert 'abcdefghij' == irc_unstyle('\x02abcdefg\x1Dhij\x02')


@pytest.mark.parametrize(
    'input_, output', [('hello', 'hello'), ('longertext', 'longer...')]
)
def test_trim_message(input_, output):
    assert output == trim_message(input_, length=9)


@mock.patch('chitanda.util.sys')
@mock.patch('chitanda.bot.Chitanda')
def test_register_decorator(chitanda, sys):
    chitanda.commands = {}
    sys.modules = {'hello': 12345}
    register('trigger')(mock.Mock(__module__='hello'))
    assert chitanda.commands['trigger'] == 12345


def test_args_decorator():
    func = mock.Mock()
    args(re.compile('a(bc)$'), ' meow')(func)(message='abc')
    assert func.call_args[1]['args'] == ('bc',)


def test_args_decorator_error():
    with pytest.raises(BotError):
        args('a$')(mock.Mock())(message='bark')


@pytest.mark.asyncio
async def test_admin_only_decorator_generator():
    async def func(*args, **kwargs):
        for n in [1, 2, 3]:
            yield n

    listener = mock.Mock()
    listener.is_admin.side_effect = coroutine(lambda *args, **kwargs: True)
    assert [1, 2, 3] == [
        n async for n in admin_only(func)(listener=listener, author='daz')
    ]


@pytest.mark.asyncio
async def test_admin_only_decorator_not_generator():
    listener = mock.Mock()
    listener.is_admin.side_effect = coroutine(lambda *args, **kwargs: True)
    func = mock.Mock(side_effect=coroutine(lambda *args, **kwargs: 'hello'))
    assert 'hello' == await admin_only(func)(listener=listener, author='daz')


@pytest.mark.asyncio
async def test_admin_only_decorator_error():
    listener = mock.Mock()
    listener.is_admin.side_effect = coroutine(lambda *args, **kwargs: False)
    with pytest.raises(BotError):
        await admin_only(mock.Mock())(listener=listener, author='daz')


@pytest.mark.asyncio
async def test_auth_only_decorator_generator():
    async def func(*args, **kwargs):
        for n in [1, 2, 3]:
            yield n

    listener = mock.Mock()
    listener.is_authed.side_effect = coroutine(lambda *args, **kwargs: True)
    assert [1, 2, 3] == [
        n async for n in auth_only(func)(listener=listener, author='daz')
    ]


@pytest.mark.asyncio
async def test_auth_only_decorator_not_generator():
    listener = mock.Mock()
    listener.is_authed.side_effect = coroutine(lambda *args, **kwargs: True)
    func = mock.Mock(side_effect=coroutine(lambda *args, **kwargs: 'hello'))
    assert 'hello' == await auth_only(func)(listener=listener, author='daz')


@pytest.mark.asyncio
async def test_auth_only_decorator_error():
    listener = mock.Mock()
    listener.is_authed.side_effect = coroutine(lambda *args, **kwargs: False)
    with pytest.raises(BotError):
        await auth_only(mock.Mock())(listener=listener, author='daz')


def test_channel_only_decorator():
    func = mock.Mock(return_value='hello')
    assert 'hello' == channel_only(func)(private=False)


def test_channel_only_decorator_error():
    with pytest.raises(BotError):
        channel_only(mock.Mock())(private=True)


def test_private_message_only_decorator():
    func = mock.Mock(return_value='hello')
    assert 'hello' == private_message_only(func)(private=True)


def test_private_message_only_decorator_error():
    with pytest.raises(BotError):
        private_message_only(mock.Mock())(private=False)


def test_allowed_listeners_decorator_none():
    func = mock.Mock(return_value='hello')
    assert 'hello' == allowed_listeners()(func)(listener=IRCListener)


def test_allowed_listeners_decorator_one():
    assert 'hello' == allowed_listeners(IRCListener)(
        mock.Mock(return_value='hello')
    )(listener=mock.Mock(spec=IRCListener))


def test_allowed_listeners_decorator_fail():
    with pytest.raises(BotError):
        allowed_listeners(IRCListener)(mock.Mock(return_value='hello'))(
            listener=mock.Mock(spec=DiscordListener)
        )
