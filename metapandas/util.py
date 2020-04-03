"""Provide utility functions used elsewhere in this package."""
from metapandas.config import VERBOSE


def _vprint(*args, **kwargs):
    """Print only when VERBOSE evaulates to true within config."""
    if VERBOSE:
        print(*args, **kwargs)
