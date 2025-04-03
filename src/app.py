import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1) Connect to the database with SQLAlchemy
def connect():
    global engine
    try:
        connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        print("Starting the connection...")
        engine = create_engine(connection_string, isolation_level="AUTOCOMMIT")
        engine.connect()
        print("Connected successfully!")
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
# 2) Create the tables
def create_tables(engine):
    try:
        with engine.connect() as connection:
            # Define the SQL commands to create tables
            create_tables_sql = """
            CREATE TABLE IF NOT EXISTS publishers (
                publisher_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                PRIMARY KEY(publisher_id)
            );

            CREATE TABLE IF NOT EXISTS authors (
                author_id INT NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                middle_name VARCHAR(50) NULL,
                last_name VARCHAR(100) NULL,
                PRIMARY KEY(author_id)
            );

            CREATE TABLE IF NOT EXISTS books (
                book_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                total_pages INT NULL,
                rating DECIMAL(4, 2) NULL,
                isbn VARCHAR(13) NULL,
                published_date DATE,
                publisher_id INT NULL,
                PRIMARY KEY(book_id),
                CONSTRAINT fk_publisher FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id)
            );

            CREATE TABLE IF NOT EXISTS book_authors (
                book_id INT NOT NULL,
                author_id INT NOT NULL,
                PRIMARY KEY(book_id, author_id),
                CONSTRAINT fk_book FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
                CONSTRAINT fk_author FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE
            );
            """
            connection.execute(create_tables_sql)
            print("Tables created successfully (if they didn't exist).")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Main function to run the steps
if __name__ == "__main__":
    engine = connect()
    if engine:
        create_tables(engine) 
df = pd.read_sql("SELECT * FROM publishers;", engine)
print(df)        