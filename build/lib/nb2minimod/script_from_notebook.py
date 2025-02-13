import nbformat
from pathlib import Path
import typer
from typing_extensions import Annotated
from typing import Optional
import re 


def first_code_line(cell):
    dir_pre = r"\s*#\s*\|"
    return min([i for i,o in enumerate(cell.split('\n')) if o.strip() != '' and not re.match(dir_pre, o)])

def split_cell(cell):
    code_lines = cell.splitlines(True)
    first_code = first_code_line(cell)
    return code_lines[:first_code], code_lines[first_code:]

def is_export(cell):
    dirs, code = split_cell(cell)
    return any('#| export\n'==d for d in dirs)

def read_and_write_to_script(nb, stem_name:Path, mod_name:str):
    code_cells = [c['source'] for c in nb['cells'] if c['cell_type']=='code']
    export_cells = [cell for cell in code_cells if is_export(cell)]

    if len(export_cells) == 0:
        return ''
    
    script_path = Path(stem_name) / (mod_name+'.py')
    with open(script_path, 'w') as f:
        #TODO duplicated functions accross
        script_globals = [f'{mod_name}_globals = globals()']

        f.write('\n\n'.join(export_cells))
        if script_path.exists():
            print((mod_name+'.py'), 'was written')
    return f'from .{mod_name} import *\n'


def main(path:Annotated[Optional[str], typer.Argument()]=None,
         folder_name:Annotated[Optional[str], typer.Argument()]=None,
         create_core:bool=True):
    """
    Take a path to either a directory or a single notebook file and generate
    a Python module from each notebook file found. The module will be given the
    same name as the notebook file, and will contain all code cells that start
    with '#| export'. The contents, (including comments) of these code cells will be in the same order
    as they appear in the notebook.

    If a directory is given, a new directory with the same name will be created
    containing all the generated Python modules. If a notebook file is given, the
    generated module will be written in the same directory.

    The __init__.py file for the new directory will be created containing import
    statements for all the generated Python modules.

    If path is None, the current directory will be used. If create_core is False,
    the __init__.py file will not be created.

    Example:
        nb2script my_notebooks
        nb2script notebook.ipynb
        nb2script my_notebooks --no-create-core
    """
    if path is None:
        path='.'
    path=Path(path)
    base_path = path.resolve()
    
    if base_path.suffix == '':
        is_dir = True
        base_stem = base_path.stem
        nb_files = base_path.glob('*.ipynb')
    else:
        is_dir = False
        base_stem = base_path.parts[-2]
        nb_files = [base_path.name]
    
    if folder_name is None:
        folder_name = base_stem

    stem_path = base_path/folder_name
    if not stem_path.exists():
        stem_path.mkdir(exist_ok=False)

    core_script = ''
    for file in nb_files:
        nb = nbformat.read(file, as_version=4)
        if is_dir:
            name = file.name.split('.')[0]
        else:
            name = file.split('.')[0]

        import_line = read_and_write_to_script(nb, stem_path, name)
        core_script += import_line

    if create_core:
        core_path = stem_path/ '__init__.py'
        with open(core_path, 'w') as f:
            f.write(core_script)
