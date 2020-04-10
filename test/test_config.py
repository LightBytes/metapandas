import os
import sys

from importlib import reload

import metapandas.config as cfg


def test_config():
    assert hasattr(cfg, 'VERBOSE')
