from models.db import MongoAPI
from flask import Flask, request, jsonify, Response

from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from utils import slugify
import time

app = Flask(__name__)
api = Api(app)
data = MongoAPI({
        "database":"<dbname>",
        "collection":"shorterrs"
    })
shorter_put_args = reqparse.RequestParser()
shorter_put_args.add_argument("slug", type=str, help="Slug")
shorter_put_args.add_argument("android_link", type=str, help="Please Enter Android Link")
shorter_put_args.add_argument("ios_link", type=str, help="Please Enter IOS Link")
shorter_put_args.add_argument("web_link", type=str, help="Please Enter WebLink")
shorter_put_args.add_argument("user_id", type=str, help="User_id")


const = "/as"
print(data.read())
class Shorter(Resource):
    def get(self, slug):
        # return jsonify(data.read())
        print(request.user_agent)
        return {'name2':'name'}

    def post(self):
        args = shorter_put_args.parse_args()
        now = time.time()

        try:
            response = data.write_short_links(slugify(now),args['ios_link'],args['android_link'],args['web_link'])
            print(response)
        except ConnectionError:
            raise ConnectionError('connection failed')

api.add_resource(Shorter,"/shorter/<slug>")

if __name__ == '__main__':
    app.run(debug=True,port=5002)
