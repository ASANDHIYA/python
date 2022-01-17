import datetime
from functools import wraps
import jwt
from flask import Flask, request, json, jsonify, make_response

# from views.category import user_auth_bp
from flask_migrate import Migrate
from models.base import Category, News, User
from models.base import db

# from models.news import db
# from views.category import user_auth_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
migrate = Migrate(app, db)
# app.register_blueprint(user_auth_bp, url_prefix="")

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # print(token)
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # print(token)
            current_user = User.query \
                .filter_by(user_role=data['user']) \
                .first()
            # print(data['user'])
        except:
            return jsonify({
                'message': 'Token is invalid !! or expiry'
            }), 401
        # returns the current logged users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


def get_jwt_identity():
    pass


@app.route('/refresh', methods=['GET'])
def refresh_token():
    pass


@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.get_json()
    # print(auth.get('email'))
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query \
        .filter_by(email=auth.get('email')) \
        .first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )
    # print(user.password)
    # print(auth.get('password'))
    if user:
        # generates the JWT Token
        # print("ggf")
        token = jwt.encode({
            'user': user.user_role, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verifyjhj',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@app.route('/category/signup/', methods=['POST', 'GET'])
def sign_Up():
    if request.method == "POST":
        if request.is_json:
            payload = request.get_json()
            # print(payload)
            # token = jwt.encode({'user': payload['user_role'], 'iat': datetime.datetime.utcnow()},
            #                    app.config['SECRET_KEY'])
            email = payload['email']
            user = User.query \
                .filter_by(email=email) \
                .first()
            # print(user)
            if not user:
                value = User(username=payload['username'], password=payload['password'], email=payload['email'],
                             user_role=payload['user_role'])
                value.save()
                # return jsonify(status='success', message='Token generated successfully', token=token.decode("utf-8"))
                return "success", 200
            else:
                return "existing user", 200


@app.route('/category/signIn/', methods=['POST', 'GET'])
@token_required
def sign_in(current_user):
    user = current_user.user_role
    # print(user)
    if user == "user" or user == "admin":
        news_views = News.query.all()
        results = [
            {
                "news_id": news1.news_id,
                "headlines": news1.headline,
                "Details": news1.Details,
                "edited_by": news1.edited_by,
                "category_id": news1.category_id
            } for news1 in news_views]

        return {"count": len(results), "news": results}
    else:
        return "invalid credentials"
    #     pass
    # # print(user.user_role)
    # return "success"


@app.route('/category/create', methods=['POST', 'GET'])
@token_required
def create_category(user):
    user = user.user_role
    if user == "admin":
        if request.method == 'POST':
            data = request.get_json()
            if request.is_json:
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
    else:
        return "access denied"


@app.route('/category/<int:cat_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_category(user, cat_id):
    user = user.user_role
    if user == "admin":
        cate = Category.query.get_or_404(cat_id)
        # print(cate)
        if request.method == 'GET':
            response = {
                "name": cate.name,
            }
            return {"message": "success", "category": response}, 200

        elif request.method == 'PUT':
            payload = request.get_json()
            # print(payload)
            cate.name = payload['name']
            cate.update()
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

        elif request.method == 'DELETE':
            cate.delete()
            # db.session.delete(cate)
            # db.session.commit()
            return {"message": f"category successfully deleted."}
    else:
        return "access denied"


@app.route("/category/news", methods=['POST', 'GET'])
@token_required
def Create_News(user):
    user = user.user_role
    # print(user)
    if request.method == 'POST':
        if request.is_json:
            if user == "admin":
                payload = request.get_json()
                # print(payload)
                # name = data['name']
                # value = News(headline=payload['headline'])
                value = News(headline=payload['headline'], Details=payload['details'], edited_by=payload['edited_by'],
                             category_id=payload['categoryid'])
                value.save()
                return {"message": f"category {value.headline} has been created successfully."}
            else:
                return {"message": "access denied"}
    elif request.method == 'GET':
        if user == "admin" or user == "user":
            news_views = News.query.all()
            results = [
                {
                    "news_id": news1.news_id,
                    "headlines": news1.headline,
                    "Details": news1.Details,
                    "edited_by": news1.edited_by,
                    "category_id": news1.category_id
                } for news1 in news_views]

            return {"count": len(results), "news": results}


@app.route('/category/update/<int:news_id>', methods=['GET', 'PUT', 'DELETE'])
def update_news(news_id):
    cate_news = News.query.get_or_404(news_id)
    # print(cate_news)
    if request.method == 'GET':
        response = {
            # "name": cate_news.name,
            "news_id": cate_news.news_id,
            "headlines": cate_news.headline,
            "Details": cate_news.Details,
            "edited_by": cate_news.edited_by,
            "category_id": cate_news.category_id
        }
        return {"message": "success", "category": response}, 200

    elif request.method == 'PUT':
        payload = request.get_json()
        print(payload)
        cate_news = News(headline=payload['headline'], Details=payload['details'], edited_by=payload['edited_by'],
                         category_id=payload['categoryid'])
        # cate_news.name = payload['name']
        cate_news.update()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    elif request.method == 'DELETE':
        cate_news.delete()
        return {"message": f" {cate_news.headline} successfully deleted."}


if __name__ == '__main__':
    app.run(debug=True)
