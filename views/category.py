# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
from flask import Blueprint, request
from models.category import Category
from api import app

user_auth_bp = Blueprint('user_auth_bp', __name__, template_folder="views", static_folder='')


@user_auth_bp.route('/')
@user_auth_bp.route('/category/create', methods=['POST', 'GET'])
def create_category():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            # print(data)
            value = Category(name=data['name'])
            # print(value)
            value.save()

            return {"message": f"category {value.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        category_create = Category.query.all()
        results = [
            {
                "id": category.id,

                "name": category.name,
            } for category in category_create]

        return {"count": len(results), "category": results}

# @bp.route("/")
# def main():
#     return 'Hello World !'
