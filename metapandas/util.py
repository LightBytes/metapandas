"""Provide utility functions used elsewhere in this package."""
from metapandas.config import VERBOSE, JSON_DUMPS_KWARGS

import sys


def _vprint(level='info', *args, **kwargs):
    """Print only when VERBOSE evaulates to true within config."""
    if VERBOSE:
        print(*args, **kwargs)


def get_major_minor_version(module):
    """Return a float of the major.minor version release of module or None."""
    try:
        version = float('.'.join(getattr(module.__version__.split('.')[:2])))
    except AttributeError:
        version = None
    return version


def get_json_dumps_kwargs(json):
    """Return dumps keyword arguments compatible with installed json version."""
    kwargs = JSON_DUMPS_KWARGS or {'indent': 2}
    if json != sys.modules.get('json'):
        jsonpickle_version = get_major_minor_version(json)
        if jsonpickle_version < 1.5:
            kwargs.pop('indent')  # not supported
    return kwargs
