from gevent import monkey  # isort:skip

monkey.patch_all()  # noqa

import click


@click.group()
def cmdgroup():
    pass
