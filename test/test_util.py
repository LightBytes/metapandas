from metapandas import util
from unittest.mock import MagicMock, Mock, patch
from contextlib import redirect_stdout

import pytest
import pandas as pd
import json
import jsonpickle


def test_firendly_symbol_name_for_module():
    name = util.friendly_symbol_name(json)
    assert isinstance(name, str)


def test_friendly_symbol_name_for_function():
    name = util.friendly_symbol_name(util.friendly_symbol_name)
    assert isinstance(name, str)
    assert name == 'metapandas.util.friendly_symbol_name'


def test_friendly_symbol_name_for_class():
    name = util.friendly_symbol_name(pd.DataFrame)
    assert isinstance(name, str)
    assert name == 'pandas.core.frame.DataFrame'


def test_get_json_dumps_kwargs_with_standard_lib_json():
    kwargs = util.get_json_dumps_kwargs(json)
    assert isinstance(kwargs, dict)
    assert 'indent' in kwargs


def test_get_json_dumps_kwargs_with_older_jsonpickle():
    with patch.object(util, 'get_major_minor_version', return_value=1.4):
        kwargs = util.get_json_dumps_kwargs(jsonpickle)
        assert isinstance(kwargs, dict)
        assert 'indent' not in kwargs


def test_get_json_dumps_kwargs_with_newer_jsonpickle():
    with patch.object(util, 'get_major_minor_version', return_value=1.5):
        kwargs = util.get_json_dumps_kwargs(jsonpickle)
        assert isinstance(kwargs, dict)
        assert 'indent' in kwargs


def test_get_major_minor_verison():
    util.get_major_minor_version


def test_mangle():
    util.mangle


def test_snake_case_upper_camel():
    snake = util.snake_case('ThisIsAStringWithUpperCamelCase')
    assert snake == 'this_is_a_string_with_upper_camel_case'

def test_vprint_VERBOSE():
    util._vprint

def test_vprint_not_VERBOSE():
    util._vprint
