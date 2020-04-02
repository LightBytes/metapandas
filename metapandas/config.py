from collections import defaultdict
import os

def parse_env_flag(var, var_default=None, cast=int, cast_default=0):
    return cast(os.environ.get(var, var_default) or cast_default))


VERBOSE = parse_env_flag('METAPANDAS_VERBOSITY')

INCLUDE_APT_PACKAGES = parse_env_flag('METAPANDAS_INCLUDE_APT_PACKAGES', 1)
INCLUDE_BREW_PACKAGES = parse_env_flag('METAPANDAS_INCLUDE_BREW_PACKAGES', 1)
INCLUDE_CONDA_PACKAGES = parse_env_flag('METAPANDAS_INCLUDE_CONDA_PACKAGES', 1)
INCLUDE_PYTHON_PACKAGE = parse_env_flag('METAPANDAS_INCLUDE_PYTHON_PACKAGES', 1)