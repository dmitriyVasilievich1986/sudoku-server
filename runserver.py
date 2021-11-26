#!/usr/bin/env python
from django.core.management import execute_from_command_line
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.transaction import get_connection
from psycopg2 import OperationalError
from os import environ
from time import sleep
import logging


def runserver(host: str, port: str, *args: tuple, **kwargs: dict) -> None:
    # make migrations and migrate
    execute_from_command_line([__name__, "makemigrations"])
    execute_from_command_line([__name__, "migrate"])

    # start server
    execute_from_command_line([__name__, "runserver", f"{host}:{port}"])


def data_base_check_connection(*args: tuple, **kwargs: dict) -> bool:
    # initialize constants
    MAX_DB_CONNECTION_TRY: int = 3
    PAUSE_LENGTH: int = 5

    # get connection settings from main django settings
    connection: BaseDatabaseWrapper = get_connection()
    # get port, host values from settings. if they exist
    db_text: str = "Host: {}, Port: {}".format(
        connection.settings_dict.get("HOST"),
        connection.settings_dict.get("PORT"),
    )

    # try to connect to db
    while MAX_DB_CONNECTION_TRY:
        try:
            connection.connect()
            logging.debug(f"Connection succeded. {db_text}")
            return True
        except OperationalError as e:
            logging.warning(
                f'Fail to connect to db. Attempts left: {MAX_DB_CONNECTION_TRY}')
            logging.warning(e.args[0])
        MAX_DB_CONNECTION_TRY = MAX_DB_CONNECTION_TRY - 1
        sleep(PAUSE_LENGTH)
    logging.error(f'Fail to connect to db. {db_text}')
    return False


if __name__ == "__main__":
    # get get host, port data from envirement
    APP_NAME: str = environ.get("APP_NAME", "app")
    HOST: str = environ.get("HOST", "0.0.0.0")
    PORT: str = environ.get("PORT", "3000")

    # set path to main settings from application
    environ.setdefault('DJANGO_SETTINGS_MODULE', f'{APP_NAME}.settings')
    # try connect to db. if succeed, then runserver
    if data_base_check_connection():
        runserver(host=HOST, port=PORT)
