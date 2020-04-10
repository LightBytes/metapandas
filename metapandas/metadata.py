"""Module for quickly adding metadata to dataset when processing."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from collections import defaultdict
from json import JSONDecodeError

import re
import os
import sys
import platform
import getpass
import logging
import datetime
import warnings
import subprocess  # nosec

import pandas as pd

from loguru import logger

from metapandas.util import get_json_dumps_kwargs

try:
    import psutil
except (ImportError, PermissionError):
    logger.error('Unable to use psutil, maybe because it requires elevated privaledges')
    psutil = None

try:
    import cpuinfo
except (ImportError, PermissionError):
    logger.error('Unable to use cpuinfo, maybe because it requires elevated privaledges')
    cpuinfo = None

try:
    import jsonpickle as json  # handle many arbitrary python objects
except ImportError:
    logger.error('Full JSON serialisation not available - please pip install jsonpickle')
    import json


class MetaData:
    """A metadata class."""

    def __init__(self, logger: Optional[logging.Logger] = None, filepath: str = 'metadata.json', **kwargs):
        """Create a new metadata object.

        Parameters
        ----------
        logger: logging.Logger or None
            Log errors to :code:`logger`. A default logger will be used if not provided.
        filepath: str
            Default filepath for JSON output to be stored.

        """
        self.logger = logger or logging.getLogger(__file__)
        self.filepath = filepath
        self.__dict__.update(kwargs)
        self.actions = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: '')), {})

    @staticmethod
    def _list_packages(cmd: str, columns: List[str],
                       ignore_first_n_lines: int = 0) -> pd.DataFrame:
        """List packages using system commands to produce output dataframes.

        This is intended to act as an internal helper method to interface
        with shell command output via subprocess calls.

        Parameters
        ----------
        cmd: str
            The shell commmand to execute to produce raw package output,
            which is then converted into a tabular format.
        columns: List[str]
            The column names for the tabular data.
        ignore_first_n_lines: int
            The number of lines of the shell command output to ignore as header lines.

        Returns
        -------
        pd.DataFrame
            The package list as a dataframe. The columns are as specified by the :code:`columns` argument.

        Notes
        -----
        When the subprocess command fails, an empty dataframe will be returned.

        """
        try:
            output_bytes = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)  # nosec
            pkgs = output_bytes.decode('utf8', errors='ignore')
            lines = re.split('[\r\n]+', re.sub('[ \t]+', ',', pkgs))[ignore_first_n_lines:]
            data = [line.split(',')[:len(columns)] for line in lines if line.strip()]
        except subprocess.CalledProcessError:
            data = []
        return pd.DataFrame(data, columns=columns)

    @classmethod
    def list_conda_packages(cls) -> pd.DataFrame:
        """List Conda packages as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            Dataframe containing package entries with the following attributes:
                1. name - The package identifier.
                2. version - The version of the source code used to build the package.
                3. build - The specific build number for the package.
                4. channel - The conda channel used to install the package.

        Notes
        -----
        When the subprocess command fails, an empty dataframe will be returned.

        """
        return cls._list_packages(cmd='conda list', ignore_first_n_lines=3,
                                  columns=['name', 'version', 'build', 'channel'])

    @classmethod
    def list_brew_packages(cls) -> pd.DataFrame:
        """List Brew packages as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            Dataframe containing package entries with the following attributes:
                1. name - The package identifier.
                2. version - The version of the source code used to build the package.

        Notes
        -----
        When the subprocess command fails, an empty dataframe will be returned.

        """
        return cls._list_packages(cmd='brew list --versions',
                                  columns=['name', 'version'])

    @classmethod
    def list_apt_packages(cls) -> pd.DataFrame:
        """List Debian APT packages as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            Dataframe containing package entries with the following attributes:
                1. name - The package identifier.
                2. version - The version of the source code used to build the package.
                3. architecture - The target cpu architecture for the package.

        Notes
        -----
        When the subprocess command fails, an empty dataframe will be returned.

        """
        df = cls._list_packages(cmd='dpkg -l', ignore_first_n_lines=5,
                                columns=['installed', 'name', 'version', 'architecture'])
        return df[df.columns[1:]]

    def register_action(self, on: Union[Path, str], action: str, description: str) -> List[str]:
        """Denote processing undertaken for :code:`filename`.

        Parameters
        ----------
        on: str|Path
            The filename (or thing) the action refer to.
        action: str
            The name of the action (group).
        description: str
            A description of the action undertaken. If a previous description is found
            for the same acion :code:`on` :code:`name` then the description is appended as a newline.

        Returns
        -------
        List[str]
            A list of actions undertaken.

        """
        self.actions[str(on)][str(datetime.datetime.now())
                              ][action] += (description.strip('\n') + '\n' if description else '')
        return ["{}: {}".format(k, ['<{ki}> {vi}'.format(**locals()) for ki, vi in v.items()])
                for k, v in self.actions[str(on)].items()]

    @classmethod
    def merge(cls, left: Dict[str, Any], right: Dict[str, Any], sep='; ') -> Dict[str, Any]:
        """Merge two metadata dictionaries together using :code:`sep`."""
        merged = left.copy()
        right = right.copy()
        merged.update({k: v for k, v in right.items() if k not in left})
        for key in [key for key in set(list(left.keys()) + list(right.keys()))
                    if key in left and key in right]:
            if isinstance(merged[key], str):
                merged[key] = '{left_key}{sep}{right_key}'.format(left_key=left[key],
                                                                  right_key=right[key],
                                                                  sep=sep)
            elif isinstance(merged[key], (list, tuple)):
                merged[key] = list(left[key]) + list(right[key])
            elif isinstance(merged[key], dict):
                merged[key] = cls.merge(left[key], right[key])
        return merged

    def get_basic_metadata(self) -> Dict[str, Any]:
        """Return basic metadata in dictionary form.

        Returns
        -------
        dict
            Dictionary of metadata information.
        """
        metadata = {
            'os': platform.system(),
            'created-by': getpass.getuser().capitalize(),
            'created-timestamp': str(datetime.datetime.now()),
            'processed-on-machine': platform.node(),
            'python-executable': sys.executable,
            'python-version': platform.python_version(),
            'python-implementation': platform.python_implementation(),
            'python-command': ' '.join(sys.argv)
        }

        if psutil:
            metadata.update({
                'cpu-cores': psutil.cpu_count(logical=False),
                'cpu-threads': psutil.cpu_count(logical=True),
            })
        metadata['environment-variables'] = {k: v for k, v in os.environ.items()
                                             if not re.match('.*(KEY|PASSWORD|TOKEN).*', k.upper())}
        try:
            os_ver = {
                'Linux': platform.linux_distribution,
                'Darwin': platform.mac_ver,
                'Windows': platform.win32_ver
            }
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')  # ignore DeprecationWarning
                metadata['system'] = ' '.join(map(str, os_ver[platform.system()]()))
        except AttributeError:
            pass

        if cpuinfo:
            metadata['cpu'] = ' @ '.join([v for k, v in cpuinfo.get_cpu_info().items()
                                          if k in ['brand', 'hz_advertised']])
        return metadata

    def get_metadata(self) -> Dict[str, Any]:
        """Create a metadata dictionary or tagging generated data with.

        Returns
        -------
        dict
            Dictionary of metadata information.

        """
        metadata = self.get_basic_metadata()
        conda_prefix = os.environ.get('CONDA_PREFIX', None)
        if conda_prefix:
            metadata['conda-environment'] = Path(conda_prefix).name
            metadata['conda-packages'] = self.list_conda_packages().set_index('name').version.to_dict()

        if platform.system() == 'Linux':
            metadata['apt-packages'] = self.list_apt_packages().set_index('name').version.to_dict()
        elif platform.system() == 'Darwin':
            try:
                metadata['brew-packages'] = self.list_brew_packages().set_index('name').version.to_dict()
            except Exception as err:
                self.logger.error('Unable to establish brew packages used due to "{}"'.format(err))
        try:
            metadata['python-packages'] = {k: str(getattr(v, '__version__', None))
                                           for k, v in sys.modules.items()
                                           if hasattr(v, '__version__') and not k.startswith('_')}
        except Exception as err:
            self.logger.error('Unable to establish python packages used due to "{}"'.format(err))

        if self.actions:
            metadata['processing-actions'] = self.actions

        return metadata

    def save_as_json(self, filepath: Optional[str] = None,
                     data: Optional[dict] = None,
                     additional_data: Optional[dict] = None,
                     exists_action: str = 'merge',
                     errors: str = 'warn'):
        """Save metadata in JSON format to disk with optional additional data.

        Parameters
        ----------
        filepath: str
            The path for the output JSON file. Uses object's filepath when not given.
        data: dict or None
            The data to write. Will call :code:`Metadata.get_metdata()` method if not given.
        additional_data: dict or None
            Extra JSON compatible dictionary to include.
        exists_action: {'merge', 'overwrite', 'raise_error'}
            What to do when the file already exists. Merging will attempt to include both old
            and new JSON data, but under separate ::'stages' keys.
        errors: {'ignore', 'warn', 'raise'}
            Action to perform on error.

        See Also
        --------
        Metadata.get_metdata

        """
        data = (data or {}).copy() if data is not None else self.get_metadata()
        data.update(additional_data or {})

        filepath = Path(filepath or self.filepath)
        filename = str(filepath).replace('/', os.sep)  # protect from py35 Path -> str bug on Windows

        if filepath.exists():
            if exists_action == 'merge':
                with open(filename) as f:
                    try:
                        original_data = json.loads(f.read())
                    except JSONDecodeError as err:
                        original_data = {}
                        if errors == 'warn':
                            warnings.warn('Error decoding JSON data for "{}" due to {}'
                                          ''.format(filepath, err))
                        elif errors == 'raise':
                            raise

                if 'stages' in original_data:
                    # extend stages list with new JSON metadata
                    data = original_data['stages'] + [data]
                else:
                    # create new top-level stages key with list of JSON metadata
                    data = {'stages': [original_data, data]}
            elif exists_action == 'raise_error':
                raise FileExistsError('{filepath} already exists'.format(**locals()))

        with open(filename, 'w') as f:
            f.write(json.dumps(data, **get_json_dumps_kwargs(json)))
