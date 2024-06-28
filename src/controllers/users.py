from flask import abort, request

from src.models.user import User


def get_users():
    users = User.get_all()

    return [user.to_dict() for user in users]


def create_user():
    data = request.get_json()

    try:
        user = User.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201


def get_user_by_id(user_id: str):
    user: User | None = User.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict()


def update_user(user_id: str):
    data = request.get_json()

    try:
        user = User.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict()


def delete_user(user_id: str):
    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")

    return "", 204
