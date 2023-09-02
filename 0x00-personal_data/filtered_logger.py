#!/usr/bin/env python3
""" This module contains a function filter_datum """
import re
import logging
import os
from typing import List
from mysql.connector import connection


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction + separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        """ initializes self """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields or []

    def format(self, record: logging.LogRecord) -> str:
        """ filters values in incoming log records using filter_datum """
        return filter_datum(self.fields,
                            RedactingFormatter.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            RedactingFormatter.SEPARATOR)


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """ returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """ returns a connector to a database """
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', "my_db")

    return connection.MySQLConnection(user=db_username,
                                      password=db_password,
                                      host=db_host,
                                      database=db_name)


def main() -> None:
    """
        retrieve all rows in the users table and display
        each row under a filtered format
    """
    logger = get_logger()
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users;")

    fields = [i[0] for i in cursor.description]
    for row in cursor.fetchall():
        message = '; '.join(f'{fields[idx]}={row[idx]}'
                            for idx in range(len(fields)))
        logger.info(message)

    cursor.close()
    db_conn.close()


if __name__ == "__main__":
    main()
