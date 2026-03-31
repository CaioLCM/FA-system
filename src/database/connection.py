from psycopg2.pool import ThreadedConnectionPool

pool = ThreadedConnectionPool(
    maxconn=10,
    minconn=1,
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432,
    database="af_db"
)