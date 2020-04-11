import unittest
from unittest.mock import Mock
from metapandas.hooks.manager import HooksManager

mock = Mock()
mock.func = lambda *x, **kw: None
mock.attr = 'ATTRIBUTE'

MOCK_HOOKS = {
    'func': {}
}


class TestHooksManager(unittest.TestCase):
    def test_HooksManager(self):
        mgr = HooksManager()

    def test_HooksManager_apply(self):
        HooksManager.apply_hooks(obj=mock,
                                 decorator_function=lambda x, **kw: x(**kw),
                                 hooks_dict=MOCK_HOOKS)

    def test_HooksManager_remove(self):
        HooksManager.remove_hooks(obj=mock,
                                  hooks_dict=MOCK_HOOKS)
        HooksManager.remove_hooks(obj=mock,
                                  hooks_dict={'test': {}})
