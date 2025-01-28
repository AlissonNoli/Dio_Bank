import sqlite3

import click
from flask import current_app, g


def get_db():
    """Get a database connection.

    This function connects to the database specified in the Flask app configuration
    if not already connected, and returns the connection.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close the database connection.

    This function closes the database connection if it exists.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize the database.

    This function initializes the database using the schema.sql file.
    """
    db = get_db()

    with current_app.open_resource('../schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables.

    This command initializes the database and prints a confirmation message.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Initialize the Flask app with database functions.

    This function registers the database functions with the Flask app.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
