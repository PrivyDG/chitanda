from pathlib import Path

import mock
import pytest
from click.testing import CliRunner

from chitanda import create_app_dirs
from chitanda.util import register, trim_message


def test_create_app_dirs(monkeypatch):
    with CliRunner().isolated_filesystem():
        config_dir = Path.cwd() / 'config'
        data_dir = Path.cwd() / 'data'
        monkeypatch.setattr('chitanda.CONFIG_DIR', config_dir)
        monkeypatch.setattr('chitanda.DATA_DIR', data_dir)

        create_app_dirs()

        assert config_dir.is_dir()
        assert data_dir.is_dir()


@pytest.mark.parametrize(
    'input_, output', [('hello', 'hello'), ('longertext', 'longer...')]
)
def test_trim_message(input_, output):
    assert output == trim_message(input_, length=9)


@mock.patch('chitanda.util.sys')
@mock.patch('chitanda.bot.Chitanda')
def test_register_command(chitanda, sys):
    chitanda.commands = {}
    sys.modules = {'hello': 12345}
    register('trigger')(mock.Mock(__module__='hello'))
    assert chitanda.commands['trigger'] == 12345
