"""Main top-level module for MetaPandas package."""

from metapandas.metadataframe import MetaDataFrame
from metapandas.metadata import MetaData
from metapandas.hooks.pandas import (
    PandasMetaDataHooks,
    pandas_read_with_metadata,
    pandas_save_with_metadata,
    read_csv,
    read_excel,
    read_feather,
    read_hdf,
    read_json,
    read_parquet,
    read_pickle,
    read_sql,
    read_sql_table,
    read_sql_query
)
