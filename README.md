# nb2minimod

From Jupyter notebooks, take all the cells that have `# export` and output them to a python script. A `__init__.py` is generated that imports * from each module.

`pip install nb2minimod`

example shown in `tests/example_project`

## CLI

`nb2minimod path/my_project/` will create a folder called `my_project` with a file for each `ipynb` file.

CLI uses typer.

`nb2minimod --help` will show the following:

## `Usage: nb2script [OPTIONS] [PATH] [FOLDER_NAME]`

Take a path to either a directory or a single notebook file and generate a Python module from each notebook file. The module will be given the same name as the notebook file, and will contain all code cells that start with `#| export`. The contents (including comments) of these code cells will be in the same order as they appear in the notebook.

If a directory is given, a new directory with the same name will be created containing all the generated Python modules. If a notebook file is given, the generated module will be written in the same directory.

The `__init__.py` file for the new directory will be created containing import statements for all the generated Python modules. If `create_core` is False, the `__init__.py` file will not be created.

If path is None, the current directory will be used.

**Examples:**
- `nb2script my_notebooks`
- `nb2script notebook.ipynb`
- `nb2script my_notebooks --no-create-core`

### Arguments
| Argument    | Description            | Default  |
|-------------|------------------------|----------|
| `path`      | [PATH]                 | [default: None] |
| `folder_name` | [FOLDER_NAME]         | [default: None] |

### Options
| Option                     | Description                                                       | Default                 |
|----------------------------|-------------------------------------------------------------------|-------------------------|
| `--create-core`, `--no-create-core` | [default: create-core]                                     |                         |
| `--install-completion`     | Install completion for the current shell.                        |                         |
| `--show-completion`        | Show completion for the current shell, to copy it or customize the installation. | |
| `--help`                   | Show this message and exit.                                      |                         |

