import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('../.env')

load_dotenv(dotenv_path=env_path)

mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv('USER'),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DATABASE")
)