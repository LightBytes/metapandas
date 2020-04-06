import unittest
import pandas as pd

from metapandas.metadataframe import MetaDataFrame


def test_MetaDataFrame_init():
    mdf = MetaDataFrame([[1, 2, 3]], columns=list('abc'))
    assert isinstance(mdf, pd.DataFrame)
    assert hasattr(mdf, 'metadata')
    assert mdf.iloc[0].to_list() == [1, 2, 3]
    assert isinstance(mdf.metadata, dict)
    assert 'constructor' in mdf.metadata.keys()
    assert set(['args', 'class', 'kwargs']) == set(mdf.metadata['constructor'].keys())
    assert mdf.metadata['constructor']['args'] == ([[1, 2, 3]], )
    assert mdf.metadata['constructor']['kwargs'] == {'columns': ['a', 'b', 'c']}
    assert mdf.metadata['constructor']['class'] == MetaDataFrame


def test_MetaDataFrame_init_from_DataFrame():
    df = pd.DataFrame([[1, 2, 3]], columns=list('abc'))
    mdf = MetaDataFrame(df)
    assert isinstance(mdf, pd.DataFrame)
    assert hasattr(mdf, 'metadata')
    assert mdf.iloc[0].to_list() == [1, 2, 3]
    assert isinstance(mdf.metadata, dict)
    assert 'constructor' in mdf.metadata.keys()
    assert set(['args', 'class', 'kwargs']) == set(mdf.metadata['constructor'].keys())
    assert mdf.metadata['constructor']['args'] == (df, )
    assert mdf.metadata['constructor']['class'] == MetaDataFrame


def test_MetaDataFrame_init_with_metadata_dict_specified():
    mdf = MetaDataFrame([[1, 2, 3]], columns=list('abc'), metadata={'extra': True})
    assert isinstance(mdf, pd.DataFrame)
    assert hasattr(mdf, 'metadata')
    assert mdf.iloc[0].to_list() == [1, 2, 3]
    assert isinstance(mdf.metadata, dict)
    assert 'extra' in mdf.metadata.keys()
    assert mdf.metadata['extra'] == True
    assert 'constructor' in mdf.metadata.keys()
    assert set(['args', 'class', 'kwargs']) == set(mdf.metadata['constructor'].keys())
    assert mdf.metadata['constructor']['args'] == ([[1, 2, 3]], )
    assert mdf.metadata['constructor']['kwargs'] == {'columns': ['a', 'b', 'c']}
    assert mdf.metadata['constructor']['class'] == MetaDataFrame