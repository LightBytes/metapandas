"""Importing this module will automatically decorate pandas."""

from metapandas.hooks.pandas import PandasMetaDataHooks

# This will get executed as part of the python module import
PandasMetaDataHooks.install_metadata_hooks()
