import os

from database_utils import sql_execute


def create_initial_db():
    # create table users
    sql_execute("""
    CREATE TABLE if not exists users (
    user_rowid INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_name TEXT,
    l1 TEXT,
    l2 TEXT    
    );
    """)

    # create table cards
    sql_execute("""
    CREATE TABLE if not exists cards (
    card_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    phrase TEXT NOT NULL,
    translations TEXT,
    context_examples TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)  
    );
    """)

    # create table sets
    sql_execute("""
    CREATE TABLE if not exists sets (
    set_id INTEGER PRIMARY KEY ,
    set_name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)    
    );
    """)

    # create table set_content
    sql_execute("""
    CREATE TABLE if not exists set_content (
    content_id INTEGER PRIMARY KEY,
    set_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (set_id) REFERENCES sets (set_id),
    FOREIGN KEY (card_id) REFERENCES cards (card_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)    
    );
    """)






if __name__ == '__main__':
    create_initial_db()
    print("Database created successfully.")