from typing import Collection
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
        output = [{item:data[item] for item in data if item != '_id'and item !="user"} for data in documents if data["slug"] == slug]
        return output
    def write_short_links(self,slug, ios_link, android_link, web_link, user):
        try:
            ts = datetime.datetime.now()
            id = ObjectId.from_datetime(ts)
            response = self.collection.insert({"_id": ObjectId(id),"slug":slug, "ios_link":ios_link,"android_link":android_link, "web_link":web_link, "user":ObjectId(user)})
            return slug
        except KeyError:
            raise ValueError('invalid inpu')
        
    def get_user(self,email):
            email = self.collection.find_one({"email": email})
            return email
    def get_user(self,data):
            email = self.collection.find_one({"email":data['email'], "password":data['password']})
            return email
    def add_user(self, info):
        try:
            ts = datetime.datetime.now()
            id=ObjectId.from_datetime(ts)
            info["_id"]= (ObjectId(id))
            info["date"] = datetime.datetime.now()
            response = self.collection.insert_one(info)
            return response
        except KeyError:
            raise ValueError
    def get_links(self,user):
        links = self.collection.find({"user":ObjectId(user)})
        res = []
        for document in links:
            dicti= {}
            for key,value in document.items():
                if not key=="_id" and not key=="user":
                    dicti[key] = value
                    
            res.append(dicti)
        print(res)
        return res
        

if __name__ =="__main__":
    data = {
        "database":"<dbname>",
        "collection":"shorterrs"
    }
    mongo_obj = MongoAPI(data)
    # mongo_obj.get_user({"email":"password@gmail.com","password":"password"})
    mongo_obj.get_links("5ffd38d43fc3c772f141409a")
    # mongo_obj.get_user({"email":"xiii@gmail.com"})
    # mongo_obj.add_user({"email":"password@gmail.com","password":"password","name":'name'})
