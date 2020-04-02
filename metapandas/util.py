from metapandas.config import VERBOSE


def _vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)
