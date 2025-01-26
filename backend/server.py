from flask import Flask, request, jsonify
from flask_cors import CORS
from config import mydb
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
CORS(app)
app.config['JWT_KEY'] = os.getenv('JWT_KEY')


def generate_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    payload = {
        "user_id": user_id,
        "exp": expiration_time
    }
    token = jwt.encode(payload, app.config['JWT_KEY'], algorithm="HS256")
    return token

@app.route('/tmp', methods=["POST"])
def tmp():
    data = request.json
    return jsonify({"success" : True}), 200

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
    usr = data.get("usr_name")
    print(pw)
    hashed_password = generate_password_hash(pw)
    try:
        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO users (email, password, user) VALUES (%s, %s, %s)", (email, hashed_password, usr))
        mydb.commit()
        print(f"User {email} registered successfully!")
        return jsonify({"success": True, "message": "User successfully created"}), 201
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




if __name__ == '__main__':
    connect_to_db()
    app.run(debug=True)