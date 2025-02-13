import typer
from .script_from_notebook import main

app = typer.Typer()

app.command()(main)

if __name__ == "__main__":
    app()