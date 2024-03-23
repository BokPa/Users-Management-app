import sql_utils
import psycopg2
import psycopg2.errors
import models
from models import User

def create_db(db):
    sql_utils.create_db(db)

def create_users_table(db):
    sql = """
    CREATE TABLE Users (
        id serial,
        username varchar(255) UNIQUE,
        hashed_password varchar(80),
        PRIMARY KEY(id)
    )"""
    try:
        sql_utils.execute_sql(sql, db)
    except psycopg2.errors.DuplicateTable:
        print(f"Table Users in '{db}' already exists.")

def create_messages_table(db):
    sql = """
        CREATE TABLE Messages (
            id serial,
            from_id int NOT NULL,
            to_id int NOT NULL,
            creation_data timestamp,
            text varchar(255),
            PRIMARY KEY(id),
            FOREIGN KEY (from_id) REFERENCES Users(id),
            FOREIGN KEY (to_id) REFERENCES Users(id)
        )"""
    try:
        sql_utils.execute_sql(sql, db)
    except psycopg2.errors.DuplicateTable:
        print(f"Table Messages in '{db}' already exists.")


if __name__ == "__main__":
    database_name = "example_database"
    create_db(database_name)
    create_users_table(database_name)
    create_messages_table(database_name)
    sql = """
    INSERT INTO Users(username,hashed_password) Values ('Tomek', 'gas233r'), ('Romek','gdsag'), ('Atomek', '2342fsdf'),
     ('Atomek', 'ddddd')
    """
    sql_utils.execute_sql(sql, database_name)
    connection = psycopg2.connect(user="postgres", password="coderslab", host="localhost", database=database_name)
    cursor = connection.cursor()
    fst = User.load_user_by_username(cursor,"Romek")
    print(fst.id)