from metapandas.hooks.pandas import (
    pandas_read_with_metadata,
    pandas_save_with_metadata,
    PandasMetaDataHooks
)

def test_install_metadata_hooks():
    PandasMetaDataHooks.install_metadata_hooks()
    PandasMetaDataHooks.install_metadata_hooks()


def test_uninstall_metadata_hooks():
    PandasMetaDataHooks.uninstall_metadata_hooks()
    PandasMetaDataHooks.uninstall_metadata_hooks()


def test_pandas_save_with_metadata():
    func = pandas_save_with_metadata(lambda *x, **kw: None)
    func()


def test_pandas_read_with_metadata():
    func = pandas_read_with_metadata(lambda **kw: None)
    func()