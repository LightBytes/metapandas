"""This is the main module for MetaPandas."""

from metapandas.metadataframe import MetaDataFrame
from metapandas.metadata import MetaData
from metapandas.hooks.pandas import PandasMetaDataHooks, pandas_read_with_metadata, pandas_save_with_metadata
