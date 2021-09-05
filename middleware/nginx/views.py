from flask_restful import Resource
from config import middleware

is_active = middleware.get("nginx").get("is_active")
data = dict(msg="please use other method to monitor nginx,such as shell ...")

# TODO
class IsAlive(Resource):
    def get(self):
        if is_active == True:
            return data

# TODO: get from access.log : pv、status_code、request_time and so on
class AccessLog(Resource):
    def get(self):
        if is_active == True:
            return data