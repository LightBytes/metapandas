# metapandas
Track metadata when using pandas via JSON.

<!--lint disable no-inline-padding-->

[![ ](https://github.com/LightBytes/metapandas/workflows/Python%20CI/badge.svg)](https://github.com/LightBytes/metapandas/actions?query=workflow%3A"Python+CI")
[![ ](https://img.shields.io/pypi/pyversions/metapandas.svg?logo=python)](https://pypi.org/pypi/metapandas/)
[![ ](https://img.shields.io/pypi/l/metapandas.svg)](https://pypi.org/pypi/metapandas/)
[![ ](https://img.shields.io/pypi/implementation/metapandas?color=seagreen)](https://pypi.org/pypi/metapandas/)
[![ ](https://img.shields.io/pypi/dm/metapandas.svg?color=yellow)](https://pypi.org/pypi/metapandas/)
[![ ](https://coveralls.io/repos/github/LightBytes/metapandas/badge.svg?branch=master)](https://coveralls.io/github/LightBytes/metapandas?branch=master)
[![codecov](https://codecov.io/gh/LightBytes/metapandas/branch/master/graph/badge.svg)](https://codecov.io/gh/LightBytes/metapandas)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/de571d98b5ed4203b6eda5f927c8835d)](https://www.codacy.com/gh/LightBytes/metapandas?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LightBytes/metapandas&amp;utm_campaign=Badge_Grade)
![ ](https://img.shields.io/pypi/v/metapandas)
![ ](https://img.shields.io/badge/dev-Open%20in%20Gitpod-blue?logo=gitpod&link=https://gitpod.io/#https://github.com/LightBytes/metapandas)

<!--lint enable no-inline-padding-->

This both extends the pandas `DataFrame` with a `MetaDataFrame` class and
can decorate commonly used pandas methods for retrieving/storing data to
include metadata by default.

```python
>>> import numpy as np
>>> import metapandas as mpd
>>> data = np.arange(9).reshape(3, 3)
>>> mdf = mpd.MetaDataFrame(data, columns=list('abc'), metadata={})
>>> from pprint import pprint
>>> pprint(mdf.metadata)
{'constructor': {'args': (array([[0, 1, 2],
       [3, 4, 5],
       [6, 7, 8]]),),
                 'class': <class 'metapandas.metadataframe.MetaDataFrame'>,
                 'kwargs': {'columns': ['a', 'b', 'c']}}}

# metadata is preserved when copied
>>> mdf.metadata['test'] = True
>>> mdf.copy().metadata.get('test')
True

# metadata is stored in a JSON when saving the dataframe to disk
>>> mdf.to_csv('test.csv', index=False)
>>> from pathlib import Path
>>> list(map(str, Path('.').glob('test.csv*')))
['test.csv', 'test.csv.meta.json']

# metadata is automatically loaded when pandas hooks are installed
# this is useful if you have existing pandas code that you want to augment with metadta
>>> from metapandas.hooks.pandas import PandasMetaDataHooks
>>> from contextlib import redirect_stdout, redirect_stderr
>>> from io import StringIO
>>> str_io = StringIO()
>>> with redirect_stderr(str_io), redirect_stdout(str_io):
...     PandasMetaDataHooks.install_metadata_hooks()
>>> print('\n'.join(str_io.getvalue().strip().split('\n')[-1:]))
Installed PandasMetaDataHooks hooks
>>> import pandas as pd
>>> new_mdf = pd.read_csv('test.csv')
>>> metadata = new_mdf.metadata
>>> pprint(metadata['storage'])
{'args': [],
 'data_filepath': 'test.csv',
 'metadata_filepath': 'test.csv.meta.json',
 'method': <function NDFrame.to_csv at ...>,
 'varargs': 'args'} 

# remove pandas decorators when no longer needed
>>> PandasMetaDataHooks.uninstall_metadata_hooks()
Uninstalled PandasMetaDataHooks hooks

# alternatively just use metapandas.read_* functions without installing hooks
>>> pprint(mpd.read_csv('test.csv').metadata['storage'])
{'args': [],
 'data_filepath': 'test.csv',
 'metadata_filepath': 'test.csv.meta.json',
 'method': <function NDFrame.to_csv at ...>,
 'varargs': 'args'} 
```

Pandas modification can be performed by importing the `auto` module as follows:

```raw
>>> import metapandas.auto
Applied hook for metapandas.metadataframe.MetaDataFrame.to_csv
Applied hook for metapandas.metadataframe.MetaDataFrame.to_excel
Applied hook for metapandas.metadataframe.MetaDataFrame.to_feather
Applied hook for metapandas.metadataframe.MetaDataFrame.to_hdf
Applied hook for metapandas.metadataframe.MetaDataFrame.to_json
Applied hook for metapandas.metadataframe.MetaDataFrame.to_parquet
Applied hook for metapandas.metadataframe.MetaDataFrame.to_pickle
Applied hook for pandas.read_csv
Applied hook for pandas.read_excel
Applied hook for pandas.read_feather
Applied hook for pandas.read_hdf
Applied hook for pandas.read_json
Applied hook for pandas.read_parquet
Applied hook for pandas.read_pickle
Applied hook for pandas.read_sql
Applied hook for pandas.read_sql_table
Applied hook for pandas.read_sql_query
Applied hook for pandas.core.frame.DataFrame.to_csv
Applied hook for pandas.core.frame.DataFrame.to_excel
Applied hook for pandas.core.frame.DataFrame.to_feather
Applied hook for pandas.core.frame.DataFrame.to_hdf
Applied hook for pandas.core.frame.DataFrame.to_json
Applied hook for pandas.core.frame.DataFrame.to_parquet
Applied hook for pandas.core.frame.DataFrame.to_pickle
Installed PandasMetaDataHooks hooks
```

## Installation

MetaPandas itself is a pure python package, but depends on pandas and the SciPy
stack. Note: It optionally uses geopandas as well, which is often difficult
to install without `conda`.

To install, simply try:

```bash
pip install metapandas
```

## Development

To set up a development environment, first create either a new virtual or
conda environment before activating it and then run the following:

```bash
git clone https://github.com/lightbytes/metapandas
cd metapandas
pip install -r requirements-dev.txt requirements-test.txt -r requirements.txt
pip install -e .
```

This will install the package in development mode. Note that is you have forked
the repo then change the URL as appropriate. 

## Documentation

Documentation can be found within the `docs/` directory. This project
uses sphinx to autogenerate API documentation by scraping python docstrings.

To generate the HTML documentation, simply do the following:

```bash
cd docs
make html
```

### PDF generation

PDF documentation is currently only supported on Ubuntu systems, but needs
additional packages to run. These can be installed by:

```bash
cd docs
chmod +x setup.sh
./setup.sh
```

PDFs can then be created with `make pdf` from within the `docs/` directory.

## Contribution Guidelines

Contributions are extremely welcome and highly encouraged. To help with consistency
please can the following areas be considered before submitting a PR for review:

  - Use `autopep8 -a -a -i -r .` to run over any modified files to ensure basic pep8 conformance,
    allowing the code to be read in a style expected for most python projects.

  - New or changed functionality should be tested, running `pytest` should



  - Try to document any new or changed functionality. Note: this project uses
    [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) for it's
    docstring documentation style.

## License

Released under MIT license.
