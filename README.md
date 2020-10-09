# metapandas
Track metadata when using pandas via JSON, utilising custom DataFrame hooks.

<!--lint disable no-inline-padding-->

[![ ](https://github.com/LightBytes/metapandas/workflows/Python%20CI/badge.svg)](https://github.com/LightBytes/metapandas/actions?query=workflow%3A"Python+CI")
[![ ](https://img.shields.io/pypi/pyversions/metapandas.svg?logo=python)](https://pypi.org/pypi/metapandas/)
[![ ](https://img.shields.io/pypi/l/metapandas.svg)](https://pypi.org/pypi/metapandas/)
[![ ](https://img.shields.io/pypi/implementation/metapandas?color=seagreen)](https://pypi.org/pypi/metapandas/)
[![ ](https://img.shields.io/pypi/dm/metapandas.svg?color=yellow)](https://pypi.org/pypi/metapandas/)
[![ ](https://coveralls.io/repos/github/LightBytes/metapandas/badge.svg?branch=master)](https://coveralls.io/github/LightBytes/metapandas?branch=master)
[![ ](https://codecov.io/gh/LightBytes/metapandas/branch/master/graph/badge.svg)](https://codecov.io/gh/LightBytes/metapandas)
[![ ](https://api.codacy.com/project/badge/Grade/de571d98b5ed4203b6eda5f927c8835d)](https://www.codacy.com/gh/LightBytes/metapandas?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LightBytes/metapandas&amp;utm_campaign=Badge_Grade)
[![ ](https://img.shields.io/codefactor/grade/github/LightSlayer/metapandas?logo=codefactor)](https://www.codefactor.io/repository/github/LightBytes/metapandas)
![ ](https://img.shields.io/pypi/v/metapandas)
[![ ](https://img.shields.io/badge/Donate-buy%20me%20a%20coffee-green?logo=Buy%20me%20a%20coffee&logoColor=white)](https://ko-fi.com/lightbytes)
![ ](https://img.shields.io/badge/dev-Open%20in%20Gitpod-blue?logo=gitpod&link=https://gitpod.io/#https://github.com/LightBytes/metapandas)
[![ ](https://camo.githubusercontent.com/52feade06f2fecbf006889a904d221e6a730c194/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/LightBytes/metapandas)
[![ ](https://img.shields.io/badge/Binder%20Launch:-Jupyter%20Lab-blue.svg?colorA=&logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/LightBytes/metapandas/master?urlpath=lab)

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

<!--lint disable list-item-bullet-indent -->

Contributions are extremely welcome and highly encouraged. To help with consistency
please can the following areas be considered before submitting a PR for review:

  - Use `autopep8 -a -a -i -r .` to run over any modified files to ensure basic pep8 conformance,
    allowing the code to be read in a style expected for most python projects.
  - New or changed functionality should be tested, running `pytest` should
  - Try to document any new or changed functionality. Note: this project uses
    [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) for it's
    docstring documentation style.

<!--lint enable list-item-bullet-indent -->

## License

Released under the MIT license.

## TODO

This package is mostly a proof of concept and as such there are a number of
areas to add to, fix and improve. Of these, the following are considered to
be of highest importance:

1. Track pandas operations such as merge, groupby, etc. within metadata (**BIG TASK**) 
2. Add user friendly documentation
3. Automated semantic versioning
4. Automated master branch update release to PyPI
5. More extensive testing
6. Improve code coverage to > 90% (stretch: > 95%)
