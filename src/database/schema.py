from .connection import pool

from src.core.asset import Asset

def init_db():
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute("""
                    
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            user_key VARCHAR UNIQUE  
        )

    """)
    conn.commit()
    cursor.execute("""
                    
        CREATE TABLE IF NOT EXISTS assets(
            ID SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            name VARCHAR,
            position NUMERIC(12, 2),
            FOREIGN KEY(user_id) REFERENCES users(id));
    
    """)
    conn.commit()
    cursor.close()
    pool.putconn(conn)


def create_user(api_key):
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO users (user_key)
            VALUES (%s);
        """, (str(api_key),)
    )
    conn.commit()
    cursor.close()
    pool.putconn(conn)

def get_users():
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    response = cursor.fetchall()
    conn.commit()
    cursor.close()
    pool.putconn(conn)
    return response