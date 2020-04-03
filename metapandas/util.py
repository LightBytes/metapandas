"""Provide utility functions used elsewhere in this package."""
import sys
import re

from typing import Optional
from metapandas.config import VERBOSE, JSON_DUMPS_KWARGS


def _vprint(*args, **kwargs):
    """Print only when VERBOSE evaulates to true within config."""
    if VERBOSE:
        print(*args, **kwargs)


def snake_case(string: str) -> str:
    """Convert upper camelcase to snake case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string)


def friendly_symbol_name(obj) -> str:
    """Return a friendly symbol name for obj."""
    obj_name = obj.__name__ if str(type(obj)) == "<class 'module'>" else obj
    return re.sub("(<|class|function| at [0-9]x[0-9A-F]{8,}|'|>)", '', str(obj_name))


def get_major_minor_version(module) -> Optional[float]:
    """Return a float of the major.minor version release of module or None."""
    try:
        version = float('.'.join(module.__version__.split('.')[:2]))
    except AttributeError:
        version = None
    return version


def mangle(name: str, prefix: str = '', suffix: str = '_original') -> str:
    """Return mangled name."""
    return '{prefix}{name}{suffix}'.format(**locals())


def get_json_dumps_kwargs(json):
    """Return dumps keyword arguments compatible with installed json version."""
    kwargs = JSON_DUMPS_KWARGS or {'indent': 2}
    if json != sys.modules.get('json'):
        jsonpickle_version = get_major_minor_version(json)
        if jsonpickle_version < 1.5:
            kwargs.pop('indent')  # not supported
    return kwargs
