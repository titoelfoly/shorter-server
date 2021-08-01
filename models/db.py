from flask import Flask , request, json, Response
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime


class MongoAPI:
    def __init__(self,data):
        self.client = MongoClient("mongodb+srv://titoelfoly:tito4631041@portofolio.dspnr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        database= data['database']
        collection= data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data
    # Get Json By Slug
    def read(self, slug):
        documents = self.collection.find()
        output = [{item:data[item] for item in data if item != '_id'} for data in documents if data["slug"] == slug]
        return output
    def write_short_links(self,slug, ios_link, android_link, web_link):
        try:
            ts = datetime.datetime.now()
            id = ObjectId.from_datetime(ts)
            response = self.collection.insert({"_id": ObjectId(id),"slug":slug, "ios_link":ios_link,"android_link":android_link, "web_link":web_link})
            return response
        except KeyError:
            raise ValueError('invalid inpu')
        return

        

if __name__ =="__main__":
    data = {
        "database":"<dbname>",
        "collection":"shorterrs"
    }
    mongo_obj = MongoAPI(data)
    mongo_obj.write_short_links('slug', 'ios_linkss','android_links','ios_links')
    print(json.dumps(mongo_obj.read("ostsssotosdentsnfs"), indent=4))