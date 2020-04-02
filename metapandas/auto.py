"""Importing this module will automatically decorate pandas."""

from metapandas.hooks.pandas import PandasMetaDataHooks

PandasMetaDataHooks.install_metadata_hooks()