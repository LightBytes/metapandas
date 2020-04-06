import unittest
from metapandas.hooks.manager import HooksManager


class TestHooksManager(unittest.TestCase):
    def test_HooksManager(self):
        mgr = HooksManager()

    def test_HooksManager_apply(self):
        HooksManager.apply_hooks

    def test_HooksManager_remove(self):
        HooksManager.remove_hooks
