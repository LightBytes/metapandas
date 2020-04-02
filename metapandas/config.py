import os

VERBOSE = bool(int(os.environ.get('METAPANDAS_VERBOSITY', None) or 0))
