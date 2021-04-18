import click
from flask import Flask

from app.cli.component_cli import ComponentCli
from app.cli.seeder_cli import SeederCli
from app.extensions import db


def init_app(app: Flask):
    @app.cli.command('component', help='Create a component structure.')
    @click.option('--name', '-n', help='Component name.')
    def create_component(name):
        component_cli = ComponentCli()
        component_cli.run_command(name)

    @app.cli.command('seed', help='Fill database with fake data.')
    def seeds() -> None:
        """Command line script for filling database with fake data."""
        seeder_cli = SeederCli()
        seeder_cli.run_command()

    @app.shell_context_processor
    def make_shell_context() -> dict:
        """Returns the shell context for an interactive shell for
        this application. This runs all the registered shell context
        processors.

        To explore the data in your application, you can start an interactive
        Python shell with the shell command. An application context will be
        active and the app instance will be imported.

        References
        ----------
        Open a Shell:
        https://flask.palletsprojects.com/en/1.1.x/cli/#open-a-shell

        Returns
        -------
        dict
            Imports available in Python shell.

        """
        return {'app': app, 'db': db}
