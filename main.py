from datetime import UTC, datetime

from flask import Flask, jsonify, request

from storage import categories, get_next_id, records, users

app = Flask(__name__)


def error_response(error_code: str, message: str, status_code: int):
    return jsonify({"error": error_code, "message": message}), status_code


# --- Healthcheck API ---


@app.route("/healthz/live", methods=["GET"])
def liveness_check():
    return jsonify({
        "status": "alive",
        "timestamp": datetime.now(UTC).isoformat(),
    }), 200


@app.route("/healthz/ready", methods=["GET"])
def readiness_check():
    return jsonify({
        "status": "ready",
        "database": "in_memory",
        "timestamp": datetime.now(UTC).isoformat(),
    }), 200


# --- User Endpoints ---


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values())), 200


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = users.get(user_id)
    if not user:
        return error_response("not_found", f"User with id {user_id} not found", 404)
    return jsonify(user), 200


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)
    if not data or not isinstance(data.get("name"), str) or not data["name"].strip():
        return error_response("invalid_request", "Field 'name' is required", 400)

    user_id = get_next_id("user")
    user = {"id": user_id, "name": data["name"].strip()}
    users[user_id] = user
    return jsonify(user), 201


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    if user_id not in users:
        return error_response("not_found", f"User with id {user_id} not found", 404)
    del users[user_id]
    return "", 204


# --- Category Endpoints ---


@app.route("/category", methods=["GET"])
def get_categories():
    return jsonify(list(categories.values())), 200


@app.route("/category", methods=["POST"])
def create_category():
    data = request.get_json(silent=True)
    if not data or not isinstance(data.get("name"), str) or not data["name"].strip():
        return error_response("invalid_request", "Field 'name' is required", 400)

    category_id = get_next_id("category")
    category = {"id": category_id, "name": data["name"].strip()}
    categories[category_id] = category
    return jsonify(category), 201


@app.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id: int):
    if category_id not in categories:
        return error_response(
            "not_found", f"Category with id {category_id} not found", 404
        )
    del categories[category_id]
    return "", 204


# --- Record Endpoints ---


@app.route("/record", methods=["POST"])
def create_record():
    data = request.get_json(silent=True)
    if not data:
        return error_response("invalid_request", "Request body must be JSON", 400)

    user_id = data.get("user_id")
    category_id = data.get("category_id")
    amount = data.get("amount")

    if user_id is None or category_id is None or amount is None:
        return error_response(
            "invalid_request",
            "Fields 'user_id', 'category_id', and 'amount' are required",
            400,
        )

    if not isinstance(user_id, int) or isinstance(user_id, bool):
        return error_response("invalid_request", "'user_id' must be an integer", 400)
    if not isinstance(category_id, int) or isinstance(category_id, bool):
        return error_response(
            "invalid_request", "'category_id' must be an integer", 400
        )

    try:
        parsed_amount = round(float(amount), 2)
    except (TypeError, ValueError):
        return error_response("invalid_request", "'amount' must be a valid number", 400)

    if parsed_amount <= 0:
        return error_response("invalid_request", "'amount' must be greater than 0", 400)

    if user_id not in users:
        return error_response("not_found", f"User with id {user_id} not found", 404)
    if category_id not in categories:
        return error_response(
            "not_found", f"Category with id {category_id} not found", 404
        )

    record_id = get_next_id("record")
    record = {
        "id": record_id,
        "user_id": user_id,
        "category_id": category_id,
        "created_at": datetime.now(UTC).isoformat(),
        "amount": parsed_amount,
    }
    records[record_id] = record
    return jsonify(record), 201


@app.route("/record/<int:record_id>", methods=["GET"])
def get_record(record_id: int):
    record = records.get(record_id)
    if not record:
        return error_response(
            "not_found", f"Record with id {record_id} not found", 404
        )
    return jsonify(record), 200


@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id: int):
    if record_id not in records:
        return error_response(
            "not_found", f"Record with id {record_id} not found", 404
        )
    del records[record_id]
    return "", 204


@app.route("/record", methods=["GET"])
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if user_id is None and category_id is None:
        return error_response(
            "invalid_request",
            "At least one query parameter ('user_id' or 'category_id') "
            "is required for filtration",
            400,
        )

    filtered = list(records.values())
    if user_id is not None:
        filtered = [r for r in filtered if r["user_id"] == user_id]
    if category_id is not None:
        filtered = [r for r in filtered if r["category_id"] == category_id]

    return jsonify(filtered), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)