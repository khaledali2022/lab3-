from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded token for simplicity
TOKEN = "userapitoken"

# In-memory storage for users
users = []

# Middleware: Token authentication check
@app.before_request
def authenticate_token():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

# GET endpoint to fetch all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)
@app.route('/', methods=['GET'])
def hello():
    return "hello"
# POST endpoint to create a new user
@app.route("/users", methods=["POST"])
def create_user():
    user = {
        "id": len(users) + 1,
        "name": request.json.get("name"),
        "email": request.json.get("email"),
        "age": request.json.get("age")
    }
    users.append(user)
    return jsonify(user), 201

# GET endpoint to fetch a specific user by id
@app.route("/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(user)

# PUT endpoint to update an existing user by id
@app.route("/users/<int:id>", methods=["PUT"])
def update_user_by_id(id):
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"error": "Not Found"}), 404
    user["name"] = request.json.get("name", user["name"])
    user["email"] = request.json.get("email", user["email"])
    user["age"] = request.json.get("age", user["age"])
    return jsonify(user)

# DELETE endpoint to delete a user by id
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user_by_id(id):
    global users
    users = [user for user in users if user["id"] != id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
