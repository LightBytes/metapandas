"""Provides decorator functions for modifying pandas."""
from functools import wraps
from contextlib import redirect_stdout, redirect_stderr

import os
import sys
import inspect

import pandas as pd
import jsonpickle as json

from metapandas.util import _vprint
from metapandas.metadata import MetaData
from metapandas.metadataframe import MetaDataFrame
from metapandas.hooks.manager import HooksManager


def pandas_read_with_metadata(function=None, argname='path', **meta_kwargs):
    """Decorate pandas read function to track JSON metadata."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = MetaDataFrame(func(*args, **kwargs))

            # get default metadata
            metadata = getattr(result, 'metadata', {})
            metadata.update({
                'constructor': {
                    'class': MetaDataFrame,
                    'args': args,
                    'kwargs': kwargs
                }
            })
            try:
                metapath = None
                if meta_kwargs.get('argname_is_path', None) is False:
                    metadata.update({
                        argname: kwargs.get(argname, args[0])
                    })
                else:
                    datapath = kwargs.get(argname, args[0])
                    metapath = str(datapath).replace('/', os.sep) + '.meta.json'

                    # load additional metadata and combine
                    with open(metapath) as metafile:
                        metadata.update({
                            'data_filepath': datapath,
                            'metadata_filepath': metapath
                        })
                        metadata.update(json.loads(metafile.read()))
            except IOError as err:
                _vprint('Could not load metadata from {} due to {!r}'.format(metapath, err), file=sys.stderr)
            except Exception as err:
                _vprint('Error setting up metadata due to {!r}'.format(err), file=sys.stderr)
            finally:
                result.metadata = metadata
            return result
        return wrapper

    return decorator if function is None else decorator(function)


def pandas_save_with_metadata(function=None, argname='path',
                              metadata=MetaData(), **meta_kwargs):
    """Decorate a pandas.to_*() function to additionally store metadata."""
    data = meta_kwargs.pop('data', None)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                additional_data = getattr(args[0], 'metadata', {})
            except IndexError:  # no arguments given!
                additional_data = {}
            arginfo = inspect.getargvalues(sys._getframe(0))
            additional_data.update({
                'storage': {
                    'method': func,
                    **{attr: getattr(arginfo, attr) for attr in dir(arginfo)
                       if attr in ('args', 'varargs', 'kwargs')}
                }
            })
            additional_data.update()
            result = func(*args, **kwargs)
            metapath = None
            try:
                datapath = kwargs.get(
                    argname, args[0] if not isinstance(
                        args[0], (pd.DataFrame, pd.Series)) else args[1])
                metapath = str(datapath).replace('/', os.sep) + '.meta.json'
                additional_data['storage'].update({
                    'data_filepath': datapath,
                    'metadata_filepath': metapath,
                })
                metadata.save_as_json(filepath=metapath, data=data,
                                      additional_data=additional_data)
            except IndexError:
                pass  # unable to establish filename, so skip
            except Exception as err:
                _vprint('Could not save metadata to {} due to {!r}'.format(metapath, err), file=sys.stderr)
                raise
            return result
        return wrapper

    return decorator if function is None else decorator(function)


class PandasMetaDataHooks(HooksManager):
    """Class for handling MetaData transparently alongside ordinary Pandas using method decorators.

    Attributes
    ----------
    PANDAS_DATAFRAME_SAVE_HOOKS: Dict[str, dict]
        A dictionary of pandas.DataFrame method names as keys and kwargs as
        the values to pass to the pandas_save_with_metadata() decorator.
    PANDAS_READ_HOOKS: Dict[str, dict]
        A dictionary of pandas module-level method names as keys and kwargs as
        the values to pass to the pandas_read_with_metadata() decorator.

    """

    PANDAS_DATAFRAME_SAVE_HOOKS = {
        'to_csv': {'argname': 'path_or_buf'},
        'to_excel': {'argname': 'excel_writer'},
        'to_feather': {'argname': 'fname'},
        'to_hdf': {'argname': 'path_or_buf'},
        'to_json': {'argname': 'path_or_buf'},
        'to_parquet': {'argname': 'fname'},
        'to_pickle': {'argname': 'path'}
    }

    PANDAS_READ_HOOKS = {
        'read_csv': {'argname': 'filepath_or_buffer'},
        'read_excel': {'argname': 'io'},
        'read_feather': {'argname': 'path'},
        'read_hdf': {'argname': 'path_or_buf'},
        'read_json': {'argname': 'path_or_buf'},
        'read_parquet': {'argname': 'path'},
        'read_pickle': {'argname': 'path'},
        'read_sql': {'argname': 'sql', 'argname_is_path': False},
        'read_sql_table': {'argname': 'table_name', 'argname_is_path': False},
        'read_sql_query': {'argname': 'sql', 'argname_is_path': False},
    }

    @classmethod
    def install_metadata_hooks(cls):
        """Install Pandas metadata hooks."""
        pd = sys.modules['pandas']
        applied_pd_hooks = cls.apply_hooks(pd, pandas_read_with_metadata, cls.PANDAS_READ_HOOKS)
        applied_df_hooks = cls.apply_hooks(pd.DataFrame, pandas_save_with_metadata, cls.PANDAS_DATAFRAME_SAVE_HOOKS)
        if applied_pd_hooks or applied_df_hooks:
            _vprint('Installed {} hooks'.format(cls.__name__), file=sys.stderr)
        else:
            _vprint('*** {} hooks already installed ***'.format(cls.__name__), file=sys.stderr)

    @classmethod
    def uninstall_metadata_hooks(cls):
        """Remove Pandas metadata hooks."""
        pd = sys.modules['pandas']
        removed_pd_hooks = cls.remove_hooks(pd, cls.PANDAS_READ_HOOKS)
        removed_df_hooks = cls.remove_hooks(pd.DataFrame, cls.PANDAS_DATAFRAME_SAVE_HOOKS)
        if removed_pd_hooks or removed_df_hooks:
            _vprint('Uninstalled {} hooks'.format(cls.__name__), file=sys.stderr)
        else:
            _vprint('*** No {} hooks installed ***'.format(cls.__name__), file=sys.stderr)


# Now decorate MetaDataFrame to use metadata save decorators
with open(os.devnull, 'w') as devnull:
    with redirect_stdout(devnull), redirect_stderr(devnull):
        PandasMetaDataHooks.apply_hooks(MetaDataFrame, pandas_save_with_metadata,
                                        PandasMetaDataHooks.PANDAS_DATAFRAME_SAVE_HOOKS)

# add decorated pandas methods to module symbols
for method, meta_kwargs in PandasMetaDataHooks.PANDAS_READ_HOOKS.items():
    func_method = getattr(pd, method, None)
    if func_method is None:
        _vprint('Warning: No such attribute to decorate: "pd.{}"'.format(method), file=sys.stderr)
    globals()[method] = pandas_read_with_metadata(func_method, **meta_kwargs)
