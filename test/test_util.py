# nosec
from metapandas import util
from unittest.mock import Mock, patch
from contextlib import redirect_stdout
from metapandas import config
from io import StringIO

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


def test_get_major_minor_verison_no_version_defined():
    mock = Mock()
    assert util.get_major_minor_version(mock) is None


def test_get_major_minor_verison_version_defined():
    mock = Mock()
    mock.__version__ = '1.2.8b2'
    assert util.get_major_minor_version(mock) == 1.2


def test_mangle():
    mangled = util.mangle('test')
    assert mangled == 'test' + '_original'

def test_mangle_with_prefix():
    mangled = util.mangle('test', prefix='abc')
    assert mangled == 'abc' + 'test' + '_original'


def test_mangle_with_prefix_no_suffix():
    mangled = util.mangle('test', prefix='abc', suffix='')
    assert mangled == 'abc' + 'test'


def test_mangle_with_suffix():
    mangled = util.mangle('test', suffix='end')
    assert mangled == 'test' + 'end'


def test_mangle_with_suffix_and_prefix():
    mangled = util.mangle('test', prefix='start_', suffix='_end')
    assert mangled == ('start_' + 'test' + '_end')


def test_snake_case_upper_camel():
    snake = util.snake_case('ThisIsAStringWithUpperCamelCase')
    assert snake == 'this_is_a_string_with_upper_camel_case'


def test_snake_case_lower_camel():
    snake = util.snake_case('thisIsAStringWithUpperCamelCase')
    assert snake == 'this_is_a_string_with_upper_camel_case'


def test_vprint_VERBOSE():
    config.VERBOSE = True
    stream = StringIO()
    assert not stream.getvalue()
    with redirect_stdout(stream):
        util._vprint('Hello world', end='')
    assert stream.getvalue() == 'Hello world'


def test_vprint_not_VERBOSE():
    config.VERBOSE = False
    stream = StringIO()
    assert not stream.getvalue()
    with redirect_stdout(stream):
        util._vprint('Hello world', end='')
    assert not stream.getvalue()
