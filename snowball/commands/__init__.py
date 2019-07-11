import importlib
import sys
from pkgutil import iter_modules


def load_commands(bot):
    for name in _get_module_names():
        importlib.import_module(name)
        if hasattr(sys.modules[name], 'setup'):
            sys.modules[name].setup(bot)


def reload_commands():
    for name in _get_module_names():
        if name in sys.modules:
            importlib.reload(sys.modules[name])
        else:
            importlib.import_module(sys.modules[name])


def _get_module_names(pkg_path=__name__):
    for module_info in iter_modules(sys.modules[pkg_path].__path__):
        modname = f'{pkg_path}.{module_info.name}'
        if module_info.ispkg:
            importlib.import_module(modname)
            for modname_ in _get_module_names(modname):
                yield modname_
        yield modname
