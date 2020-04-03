"""This module is for controlling the configuration settings of MetaPanda.

It currently uses environment variables to set the default behaviour, however
at some future point it would be good to use a combination of configuration files
and environment variables, with the following precendence:

  1. shell environment variables
  2. YAML config, e.g. ~/.metapandas/config.yml

"""
import os


def parse_env_flag(var, var_default=None, cast=int, cast_default=0):
    """Helper function to parse environment variable flags.

    Parameters
    ----------
    var: str
        The environment variable name to query.
    var_default: Optional[Any]
        The default value of the environment variable if not found.
    cast: Callable
        A function which transforms the environment variable string
        into a python type.
    cast_default: Any
        The default input value for cast.

    Returns
    -------
    Any
        The environment variable as a :code:`cast` type.

    """
    return cast(os.environ.get(var, var_default) or cast_default)


VERBOSE = parse_env_flag('METAPANDAS_VERBOSITY', 1)

INCLUDE_APT_PACKAGES = parse_env_flag('METAPANDAS_INCLUDE_APT_PACKAGES', 1)
INCLUDE_BREW_PACKAGES = parse_env_flag('METAPANDAS_INCLUDE_BREW_PACKAGES', 1)
INCLUDE_CONDA_PACKAGES = parse_env_flag('METAPANDAS_INCLUDE_CONDA_PACKAGES', 1)
INCLUDE_PYTHON_PACKAGE = parse_env_flag('METAPANDAS_INCLUDE_PYTHON_PACKAGES', 1)

JSON_DUMPS_KWARGS = parse_env_flag('METAPANDAS_JSON_DUMPS_KWARGS', {}, dict, {})
