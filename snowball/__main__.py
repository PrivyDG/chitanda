import asyncio

import config
from snowball.bot import Snowball
from snowball.tasks import huey


def main():
    huey.start()

    bot = Snowball(
        config.NICKNAME,
        username=config.NICKNAME,
        realname=config.NICKNAME,
    )

    asyncio.ensure_future(
        bot.connect(
            config.IRC_HOST,
            config.IRC_PORT,
            tls=config.IRC_TLS,
            tls_verify=config.IRC_TLS_VERIFY,
        )
    )

    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
