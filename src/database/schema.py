from .connection import pool

from src.core.asset import Asset

def init_db():
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute("""
                    
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            user_key VARCHAR UNIQUE,
            strategy VARCHAR  
        );

    """)
    conn.commit()
    cursor.execute("""
                    
        CREATE TABLE IF NOT EXISTS assets(
            ID SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            name VARCHAR,
            position NUMERIC(12, 2),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    
    """)
    conn.commit()
    cursor.close()
    pool.putconn(conn)


def create_user(api_key, strategy):
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO users (user_key, strategy)
            VALUES (%s, %s);
        """, (str(api_key), strategy)
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

def get_user(user_key):
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_key = %s;", (user_key,))
    response = cursor.fetchall()
    conn.commit()
    cursor.close()
    pool.putconn(conn)
    return response

def create_asset(user_api: str, asset: Asset):
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO assets (user_id, name, position)
            SELECT id, %s, %s FROM users WHERE user_key = %s;
        """, (asset.name, asset.position, user_api)
    )
    if cursor.rowcount == 0:
        cursor.close()
        pool.putconn(conn)
        raise ValueError("user_api inválida")
    conn.commit()
    cursor.close()
    pool.putconn(conn)

def get_assets(user_api: str):
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT a.id, a.name, a.position
            FROM assets a
            JOIN users u ON a.user_id = u.id
            WHERE u.user_key = %s;
        """, (user_api,)
    )
    response = cursor.fetchall()
    print(f"olha a response: {response}")
    cursor.close()
    pool.putconn(conn)
    return response