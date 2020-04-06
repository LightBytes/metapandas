import unittest
import logging
import json

import pandas as pd

from pathlib import Path

from metapandas.metadata import MetaData

def test_init():
    md1 = MetaData()

    # check default value for filepath
    assert md1.filepath == 'metadata.json'

    # check default value for logger
    md2 = MetaData(logger=logging.getLogger())
    assert id(md1) != id(md2)
    assert md1.logger != md2.logger

    # check additional attributes
    md3 = MetaData(logger=None, more_stuff=True)
    assert md1.logger == md3.logger
    assert getattr(md3, 'more_stuff', None) is True

    # check filepath set to non-default when specified
    md3 = MetaData(logger=None, filepath='some_other_data.json')
    assert md1.logger == md3.logger
    assert md3.filepath == 'some_other_data.json'


def test_list_apt_packages():
    df = MetaData.list_apt_packages()
    assert isinstance(df, pd.DataFrame)
    assert 'name' in df.columns
    assert 'version' in df.columns


def test_list_conda_packages():
    df = MetaData.list_conda_packages()
    assert isinstance(df, pd.DataFrame)
    assert 'name' in df.columns
    assert 'version' in df.columns


def test_list_brew_packages():
    df = MetaData.list_brew_packages()
    assert isinstance(df, pd.DataFrame)
    assert 'name' in df.columns
    assert 'version' in df.columns

def test_save_as_json_defaults():
    md = MetaData()

    meta_json = Path('metadata.json')

    if meta_json.exists():
        meta_json.unlink()

    md.save_as_json()

    assert meta_json.exists()
    assert meta_json.stat().st_size > 0
    meta_json.unlink()


def test_save_as_json_data_specified():
    md = MetaData()

    meta_json = Path('metadata.json')

    if meta_json.exists():
        meta_json.unlink()

    md.save_as_json(data={})

    assert meta_json.exists()
    # NOTE: json.dump() creates two spaces due to indent=2 inside save_as_json(), so 2 bytes total
    min_size_bytes = 2
    assert meta_json.stat().st_size <= min_size_bytes
    meta_json.unlink()


def test_save_as_json_data_exists_raise_error():
    md = MetaData()

    meta_json = Path('metadata.json')

    if meta_json.exists():
        meta_json.unlink()

    meta_json.touch()
    try:
        md.save_as_json(data={}, exists_action='raise_error')
        raise AssertionError()
    except FileExistsError:
        pass

    meta_json.unlink()


def test_save_as_json_data_exists_merge_stages():
    md = MetaData()

    meta_json = Path('metadata.json')

    if meta_json.exists():
        meta_json.unlink()

    with open(str(meta_json), 'w') as f:
        json.dump({'testing': True}, f)

    md.save_as_json(data={}, exists_action='merge')

    assert meta_json.exists()

    with open(str(meta_json)) as f:
        data = json.load(f)

    assert 'stages' in data
    assert isinstance(data['stages'], list)
    assert len(data['stages']) == 2


def test_save_as_json_filepath_specified():
    md = MetaData()

    meta_json = Path('metadata1.json')

    assert str(meta_json) != str(md.filepath)

    if meta_json.exists():
        meta_json.unlink()

    md.save_as_json(filepath=meta_json)

    assert meta_json.exists()
    meta_json.unlink()


def test_get_metadata():
    md = MetaData()
    data = md.get_metadata()

    assert 'os' in data
    isinstance(data['os'], str)
    assert 'created-by' in data
    assert isinstance(data['created-by'], str)
    assert 'created-timestamp' in data
    # NOTE: there is an explicit cast of datetime to str in get_metadata()
    assert isinstance(data['created-timestamp'], str)
    assert 'processed-on-machine' in data
    assert isinstance(data['processed-on-machine'], str)
    assert 'python-executable' in data
    assert isinstance(data['python-executable'], str)
    assert 'python-version' in data
    assert isinstance(data['python-version'], str)
    assert 'python-implementation' in data
    assert isinstance(data['python-implementation'], str)
    assert 'python-command' in data
    assert isinstance(data['python-command'], str)
    assert 'cpu-cores' in data
    assert isinstance(data['cpu-cores'], int)
    assert 'cpu-threads' in data
    assert isinstance(data['cpu-threads'], int)
    assert 'system' in data
    assert isinstance(data['system'], str)
    assert 'cpu' in data
    assert isinstance(data['cpu'], str)


def test_register_action():
    md = MetaData()
    actions = md.actions.copy()
    md.register_action(on='test_env', action='do_unit_test',
                        description='test if action is recorded')
    assert actions != md.actions
    assert isinstance(md.actions, dict)
    assert len(md.actions.keys()) > len(actions.keys())
    assert 'test_env' in md.actions
    assert isinstance(md.actions['test_env'], dict)
    assert len(md.actions['test_env']) == 1

    assert 'processing-actions' in md.get_metadata()


def test_merge_metadata_dictionaries():
    d1 = {'sci-fi': 'star', 'borg': {'1of3': [1, 2]}}
    d2 = {'sci-fi': 'trek', 'ship': 'Enterprise', 'borg': {'1of3': [3]}}

    d12 = MetaData.merge(d1, d2, sep=' | ')

    # TODO: more rigorous tests
    assert len(d12) > len(d1)
    assert d12['borg']['1of3'] == [1, 2, 3]
    assert d12['sci-fi'] == 'star | trek'
