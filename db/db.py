import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_DATABASE = os.getenv("DB_DATABASE", "database")

conn = pymysql.connect(
    host=DB_HOST,
    port=int(DB_PORT),
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)

cursor = conn.cursor()
cursor.execute("SELECT user_id, tag_id, rating FROM preferences")
data = cursor.fetchall()
cursor.close()
