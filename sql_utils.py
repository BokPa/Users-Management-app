import psycopg2

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
db = "example_database"

...
import psycopg2.extras

...


def create_db(db):
    """
    Create db with given name.

    :param str db: name of db
    """
    connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST)
    connection.autocommit = True

    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {db}")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{db}' already exists.")
    connection.close()


def execute_sql(sql_code, db):
    """
    Run given sql code with psycopg2.

    :param str sql_code: sql code to run
    :param str db: name of db,

    :rtype: list
    :return: data from psycopg2 cursor as a list (can be None) if nothing to fetch.
    """
    connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=db)
    connection.autocommit = True

    with connection:
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(sql_code)
            if sql_code.upper().startswith("SELECT"):
                return [item for item in cursor]
    connection.close()