import unittest

class TestExampleProject(unittest.TestCase):
    def test_import(self):
        import example_project.example_project as example_project
        self.assertEqual(example_project.__name__, 'example_project.example_project')
        self.assertEqual(example_project.add(1,2), 3)
        self.assertEqual(example_project.say_hello(), 'Hello World')
    
    def test_functions(self):
        import example_project.example_project as example_project
        import inspect
        funcs = [n for n,o in inspect.getmembers(example_project) if inspect.isfunction(o)]
        self.assertTrue(all(f in funcs for f in ['say_hello', 'add', 'subtract']))

    def test_export_before_def(self):
        "test that the lines that start with def are preceded by #| export"
        import inspect
        import example_project.example_project.first_module as first_module
        lines = inspect.getsource(first_module).split('\n')
        first_func_line = min([i for i,l in enumerate(lines) if l.startswith('def ')])
        self.assertTrue(lines[first_func_line-1].startswith('#|'))

class TestScriptFromNotebook(unittest.TestCase):
    def test_is_dir(self):
        from nb2minimod.script_from_notebook import get_is_dir
        self.assertTrue(get_is_dir('example_project')[0])
        self.assertFalse(get_is_dir('example_project/first_module.ipynb')[0])

    def test_stem(self):
        from nb2minimod.script_from_notebook import get_is_dir
        self.assertEqual(get_is_dir('example_project')[1], 'example_project')
        self.assertEqual(get_is_dir('example_project/first_module.ipynb')[1], 'example_project')

    def test_files(self):
        from nb2minimod.script_from_notebook import get_is_dir
        from types import GeneratorType
        self.assertTrue(isinstance(get_is_dir('example_project')[2], GeneratorType))
        self.assertEqual(get_is_dir('example_project/first_module.ipynb')[2], ['first_module.ipynb'])

    def test_read_func(self):
        from nb2minimod.script_from_notebook import read_and_write_to_script
        import nbformat
        from pathlib import Path
        ep = Path('example_project')
        nb = nbformat.read(ep/'first_module.ipynb', as_version=4)
        self.assertEqual(read_and_write_to_script(nb, 'example_project', 'first_module', _write=False), 'from .first_module import *\n')
        nb = nbformat.read(ep/'working_book.ipynb', as_version=4)
        self.assertEqual(read_and_write_to_script(nb, 'example_project', 'working_book', _write=False), '')


if __name__ == '__main__':
    unittest.main()

    