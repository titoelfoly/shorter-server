from models.db import MongoAPI
from flask import Flask, request, jsonify, Response, redirect
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required , create_access_token, get_jwt_identity
from utils import slugify
import time
import json
app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "Mukhtar El-foly" 
data = MongoAPI({
        "database":"<dbname>",
        "collection":"shorterrs"
    })
auth = MongoAPI({
    "database":"<dbname>",
    "collection":"users"
    })

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response 

@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    test = auth.get_user(email)
    if test:
        return jsonify(message="User ALready Exist"), 409
    else:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user_info = dict(name=name, email=email, password=password)
        data.add_user(user_info)
        return jsonify(message="User added sucessfully"), 201
        

@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email= request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]
    test = auth.get_user({"email":email, "password":password})
    if test:
        access_token = create_access_token(identity=str(test['_id']))
        return jsonify(message="Login Succeeded!", token=access_token , user=str(test['_id']), name=test['name']), 201
    else:
        return jsonify(message="Bad Email or Password")

@app.route("/links", methods=["GET"])
@jwt_required()
def links():
    # print("before user id")
    user_id = get_jwt_identity()
    print(user_id)
    return json.dumps(data.get_links(user_id))    

@app.route("/<slug>", methods=["GET"])
def map_to_url(slug):
    # load from db where slug = slug
    # get the url from the database
    # redirect to that url
    response = data.read(slug)
    return redirect(response[0]['web_link'])
        

shorter_put_args = reqparse.RequestParser()
shorter_put_args.add_argument("slug", type=str, help="Slug")
shorter_put_args.add_argument("android_link", type=str, help="Please Enter Android Link")
shorter_put_args.add_argument("ios_link", type=str, help="Please Enter IOS Link")
shorter_put_args.add_argument("web_link", type=str, help="Please Enter WebLink")
shorter_put_args.add_argument("user", type=str, help="User_id")


class Shorter(Resource):
    def get(self, slug):
        print(slug)
        response = data.read(slug)
        # return jsonify(data.read())
        print(request.user_agent)
        print(response)
        return response

class ShorterPost(Resource):
    def post(self):
        args = shorter_put_args.parse_args()
        now = time.time()
        sluggy = slugify(now) 
        print(args)
        try:
            response = data.write_short_links(sluggy,args['ios_link'],args['android_link'],args['web_link'], args['user'])
            # returned_slug = json.dumps({"slug":sluggy})
            return jsonify(sluggy)
        except ConnectionError:
            raise ConnectionError('connection failed')
api.add_resource(Shorter,"/shorter/<slug>")
api.add_resource(ShorterPost,"/shorter/")


if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=5000)
