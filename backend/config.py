import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv('USER'),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DATABASE")
)