from flask import Blueprint,jsonify, request
from flask_restful import Api,Resource
import pandas as pd
from werkzeug.utils import secure_filename


import sys 
import os
import json


dirname = os.path.dirname(os.path.abspath(__file__))
dirname_list = dirname.split("/")[:-1]
dirname = "/".join(dirname_list)
print(dirname)
path = dirname + "/api"
print(path)
sys.path.append(path)


mod = Blueprint('api',__name__)
api = Api(mod)
df = None

from Functions import get_file,chcking,prediction

path01=dirname +"/api/tmp"


class hello(Resource):
    def get(self):
        retJson = {"status":200,"msg":"ok"}
        return jsonify(retJson)


class data(Resource):
    def post(self):
        file_rec = request.files['file']
        filename = secure_filename(file_rec.filename) 
        print(filename)
        print(path01)
        file_path =  path01 +"/" + filename
        file_rec.save(file_path)
        print("file saved here: ",file_path)
        


        chk=get_file(file_rec,file_path)
        if chk==True:
            ret= chcking()
            os.remove(file_path)
            return jsonify(ret)
        else:
            retJson = {"status":301,"msg":"This file format is not supported"}
            os.remove(file_path)
            return jsonify(retJson)

class Prediction(Resource):
    def post(self):
        postedData=request.get_json()
        print(postedData)
        msg=postedData['Message_Size']
        
        msg1=postedData['Incoming_Header_lines_Count']
        msg2=postedData['Number_of_complaints_(BCL)']
        msg3=postedData['Sender_IP']
       
        ret=prediction(msg,msg1,msg2)
        #ret=str(ret[0])
        return jsonify(ret)
  


api.add_resource(hello, "/hello")
api.add_resource(data, "/data")
api.add_resource(Prediction, "/pred")