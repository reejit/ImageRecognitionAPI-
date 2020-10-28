"""
Image Recognition API using Deep learning
------------------------------------------

* Registration of a user with 6 tokens initially.
* Detect similarity between text1 and text2 then return ratio database for 1 token and .
* Admin can refill tokens.

@author Hamza Arain
@version 0.0.1v
@date 29 October 2020

"""

# Import modules
## Api related modules
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

## database related
from pymongo import MongoClient

## password encryption related 
import bcrypt

## Deep learning: Image classifier
import numpy
import tensorflow as tf
import requests

## Operations related
import subprocess
import json


# ###########################################################
# #######################  Tool Class ######################
# ###########################################################    

class Tool():
    def JSONOutputMessage(statusCode, output=""):
        """Return status code 200 & output"""
        retMap = {
                'Message': output,
                'Status Code': statusCode
            }
        return jsonify(retMap)


    def verifyPw(username, password):
        """varify password from database"""
        hashed_pw = users.find({
            "Username":username
        })[0]["Password"]

        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            return True
        else:
            return False

    def UserExist(username):
        """Check the existance of user"""
        if users.find({"Username":username}).count() == 0:
            return False
        else:
            return True

    def verifyCredentials(username, password):
        if not Tool.UserExist(username):
            return self.JSONOutputMessage(statusCode=301, output="Invalid Username"), True

        correct_pw = Tool.verifyPw(username, password)

        if not correct_pw:
            return self.JSONOutputMessage(statusCode=302, output="Incorrect password"), True

        return None, False



# ###########################################################
# #######################  API Classes ######################
# ###########################################################    

class Register(Resource):
    """Register user"""
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"

        if Tool.UserExist(username):
            return Tool.JSONOutputMessage(statusCode=301, output="Invalid Username")

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens":10
        })

        return Tool.JSONOutputMessage(statusCode=200, output="You successfully signed up for the API")


class Classify(Resource):
    """Image classifier"""
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]

        retJson, error = Tool.verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        tokens = users.find({
            "Username":username
        })[0]["Tokens"]

        if tokens<=0:
            Tool.JSONOutputMessage(statusCode=303, output="Not enough tokens")

        r = requests.get(url)
        retJson = {}
        with open('temp.jpg', 'wb') as f:
            f.write(r.content)
            proc = subprocess.Popen('python3 classify_image.py --model_dir=. --image_file=temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                retJson = json.load(g)

        users.update({
            "Username": username
        },{
            "$set":{
                "Tokens": tokens-1
            }  
        })
        return retJson


class Refill(Resource):
    """Refill no. tokens by admin"""
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        amount = postedData["refill"]

        if not Tool.UserExist(username):
            return Tool.JSONOutputMessage(statusCode=301, output="Invalid Username")

        correct_pw = "abc123"
        if not password == correct_pw:
            return Tool.JSONOutputMessage(statusCode=302, output="Incorrect Password")

        users.update({
            "Username": username
        },{
            "$set":{
                "Tokens": amount
            }
        })
        
        return Tool.JSONOutputMessage(statusCode=200, output="Refilled")


# ###########################################################
# ##################### Run Application #####################
# ###########################################################


# Database connection
# # "db" is same as written in web Dockerfile
# # "27017" is default port for MongoDB 
client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

# App & API creation
app = Flask(__name__)
api = Api(app)

# API paths
api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__=="__main__":
    app.run(host='0.0.0.0')
