import psycopg2
from psycopg2.pool import SimpleConnectionPool
import config  

pool = None

def init_pool():
    global pool
    try:
        pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )
        print("Database connection pool created.")
    except Exception as e:
        print(f"Error creating connection pool: {e}")

def get_conn():
    return pool.getconn()

def release_conn(conn):
    pool.putconn(conn)

def create_tables():
    if pool is None:
        print("Skipping table creation: Pool not initialized.")
        return

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id INT,
        tx_id TEXT,
        time_step INT,
        features JSONB,
        ml_probability FLOAT,
        rule_score FLOAT,
        total_rule_score FLOAT,
        fired_rules JSONB,
        final_decision BOOLEAN,
        status VARCHAR(20) DEFAULT 'PENDING',
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    conn.commit()
    cur.close()
    release_conn(conn)
    print("Tables checked/created.")