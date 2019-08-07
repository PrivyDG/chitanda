from chitanda import create_app_dirs
from chitanda.commands import cmdgroup
from chitanda.database import (
    confirm_database_is_updated,
    create_database_if_nonexistent,
)


def run():
    create_app_dirs()
    create_database_if_nonexistent()
    confirm_database_is_updated()
    cmdgroup()


if __name__ == '__main__':
    run()
