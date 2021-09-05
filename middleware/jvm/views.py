from flask_restful import Resource
from config import middleware

is_active = middleware.get("jvm").get("is_active")
data = dict(msg="please use other method to monitor jvm heap or gc,such as shell ...")

class Heap(Resource):
    def get(self):
        if is_active == True:
            return data

class GC(Resource):
    def get(self):
        if is_active == True:
            return data
