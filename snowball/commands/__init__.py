import importlib
import os
import sys
from pathlib import Path


def module_names():
    for module_path in Path(__file__).parent.iterdir():
        if module_path.suffix == '.py':
            yield os.path.splitext(module_path.name)[0]


def load_commands():
    for name in module_names():
        importlib.import_module(f'snowball.commands.{name}')


def reload_commands():
    for name in module_names():
        importlib.reload(sys.modules[f'snowball.commands.{name}'])
