from .connection import pool

from src.core.asset import Asset

def init_db():
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute("""
                    
        CREATE TABLE IF NOT EXISTS assets(
            id SERIAL,
            name VARCHAR,
            position FLOAT           
        )

    """)
    conn.commit()
    cursor.close()
    pool.putconn(conn)

