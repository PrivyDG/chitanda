import importlib
import sys
from pkgutil import iter_modules

from chitanda.config import config


def load_commands(bot, run_setup=True):
    for name in _get_module_names():
        if not _is_module_enabled(name):
            if name in sys.modules:
                del sys.modules[name]
        else:
            if name in sys.modules:
                importlib.reload(sys.modules[name])
            else:
                importlib.import_module(name)

            if run_setup and hasattr(sys.modules[name], 'setup'):
                sys.modules[name].setup(bot)


def _is_module_enabled(full_name):
    try:
        name = full_name.replace('chitanda.modules.', '', 1).split('.')[0]
        return (
            not config['modules_enabled'] or name in config['modules_enabled']
        )
    except IndexError:
        return True


def _get_module_names(pkg_path=__name__, bot=None):
    for module_info in iter_modules(sys.modules[pkg_path].__path__):
        name = f'{pkg_path}.{module_info.name}'
        if module_info.ispkg:
            importlib.import_module(name)
            for name_ in _get_module_names(name, bot=bot):
                yield name_
        yield name
