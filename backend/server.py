from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/tmp', methods=["POST"])
def tmp():
    data = request.json
    return jsonify({"success" : True}), 200

if __name__ == '__main__':
    app.run(debug=True)