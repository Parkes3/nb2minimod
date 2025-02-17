from nb2minimod.script_from_notebook import *
import unittest

source = """#| export
def foo(): return 'foo'"""

class TestSource(unittest.TestCase):
    def test_split_cell(self):
        self.assertEqual(split_cell(source), (['#| export\n'], ['def foo(): return \'foo\'']))

    def test_is_export(self):
        self.assertTrue(is_export(source))
        self.assertFalse(is_export('def foo(): return \'foo\''))
    


if __name__ == '__main__':
    unittest.main()