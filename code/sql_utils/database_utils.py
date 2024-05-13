import os
from sqlalchemy import create_engine, bindparam, text
import functools
import argparse
import sqlalchemy

parser = argparse.ArgumentParser()
parser.add_argument('-db_path', type=str,
                    help='Path to the DB', default='../data/db_backups/smart_card.db')

args = parser.parse_args()
SQL_CONNECTION_STRING = "sqlite:///" + args.db_path
# SQL_CONNECTION_STRING = "sqlite:///" + os.path.abspath("island.db")

def create_sql_connection():
    """
    Creates a new sql connection
    """
    sql_engine = create_engine(SQL_CONNECTION_STRING)

    sql_connection = sql_engine.connect()
    return sql_connection


# def with_sql_connection(func):
#     """
#     Decorator to make sure db connection objects are created and terminated appropriately
#     :param func: Function to be decorated
#     """
#
#     @functools.wraps(func)
#     def wrapper_function(*args, **kwargs):
#         connection_needs_to_be_closed = False
#         sql_connection = create_sql_connection()
#         result = func(*args, sql_connection=sql_connection, **kwargs)
#         sql_connection.close()
#         return result
#
#     return wrapper_function

def with_sql_connection():
    """
    Wrapper to make sure db connection objects are created and terminated appropriately
    :param func: Function
    :return:
    """

    # https://lemonfold.io/posts/2022/dbc/typed_decorator/
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            connection_needs_to_be_closed = False
            sql_connection = create_sql_connection()
            connection_needs_to_be_closed = True
            if not 'sql_connection' in kwargs:
                result = func(*args, sql_connection=sql_connection, **kwargs)
            else:
                result = func(*args, **kwargs)

            if connection_needs_to_be_closed:
                # sql_connection.execute('PRAGMA analysis_limit=400;')
                # sql_connection.execute("PRAGMA optimize;")
                sql_connection.commit()
                sql_connection.close()
            return result

        return wrapper

    return decorator


def bind_list_params(query, **kwargs):
    query = sqlalchemy.text(query)

    params = {}
    for key, value in kwargs.items():
        params[key] = value
        if isinstance(value, list):
            query = query.bindparams(bindparam(key, expanding=True))
    return query, params


@with_sql_connection()
def sql_execute(query, sql_connection, **kwargs):
    """
    Executes an SQL statement on the database.
    :param query: string
    :return:
    """
    query, params = bind_list_params(query, **kwargs)
    result_proxy = sql_connection.execute(query, params)
    if result_proxy.returns_rows:
        res = result_proxy.fetchall()
        result_proxy.close()
    else:
        res = None
    return res


if __name__ == '__main__':
    create_sql_connection()