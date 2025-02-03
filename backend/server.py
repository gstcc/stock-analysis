from flask import Flask, request, jsonify
from flask_cors import CORS
from config import mydb
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from dotenv import load_dotenv
import requests
from pathlib import Path

env_path = Path('../.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.config['JWT_KEY'] = os.getenv('JWT_KEY')
CORS(app)


def generate_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    payload = {
        "user_id": user_id,
        "exp": expiration_time
    }
    token = jwt.encode(payload, app.config['JWT_KEY'], algorithm="HS256")
    return token

def get_user_from_token(token):
    try:
        payload = jwt.decode(token, app.config['JWT_KEY'], algorithms=["HS256"])
        user_id = payload.get("user_id")
        return {"success" : True, "user_id": user_id}
    except jwt.ExpiredSignatureError:
        return {"success" : False, "error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"success" : False, "error": "Invalid token"}

def connect_to_db():
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT DATABASE();")  # Query to get the current database
        current_db = mycursor.fetchone()
        print(f"Connected to the database: {current_db[0]} successfully!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")


@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    email = data.get("email")
    pw = data.get("password")
    usr = data.get("user")
    hashed_password = generate_password_hash(pw)
    try:
        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO users (email, password, user) VALUES (%s, %s, %s)", (email, hashed_password, usr))
        mydb.commit()
        print(f"User {email} registered successfully!")
        mycursor.execute("SELECT id FROM users WHERE email = %s", (email))
        result = mycursor.fetchone()
        mycursor.execute("INSERT INTO userStocks (id) VALUES (%s)", (result[0])) #Also insert user to keep track of their stocks
        token = generate_token(result[0])
        return jsonify({"success": True, "message": "User successfully created", "token": token}), 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"success": False, "message": e}), 400


@app.route("/login", methods=["POST"])
def login_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Find the user by email
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    result = mycursor.fetchone()
    print(result)

    if result and check_password_hash(result[1], password):
        # User found and password matches, generate a JWT token
        user_id = result[0]
        token = generate_token(user_id)
        return jsonify({"success": True, "token": token}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/home", methods=["GET"])
def home():
    if 'token' in request.cookies:
        token = request.cookies.token
        msg = get_user_from_token(token)
        if (msg.success):
            mycursor = mydb.cursor()
            mycursor.execute("SELECT stocks FROM userStocks WHERE id = %s", (msg.user_id))
            result = mycursor.fetchall()
            print(result)
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

#Example
def tmp():
    api_key = os.getenv("API_KEY")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    print(data)

if __name__ == '__main__':
    connect_to_db()
    app.run(debug=True)