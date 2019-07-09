import importlib
import os
import sys
from pathlib import Path


def get_module_names():
    for module_path in Path(__file__).parent.iterdir():
        if module_path.suffix == '.py':
            yield os.path.splitext(module_path.name)[0]


def load_commands():
    for name in get_module_names():
        importlib.import_module(f'snowball.commands.{name}')


def reload_commands():
    for name in get_module_names():
        module_name = f'snowball.commands.{name}'
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        else:
            importlib.import_module(sys.modules[module_name])
