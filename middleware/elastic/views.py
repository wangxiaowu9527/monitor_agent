from flask_restful import Resource
from config import middleware
from utils import logger
import requests

elastic = middleware.get("elasticsearch")
is_active = elastic.get("is_active")
host = elastic.get("host")
port = elastic.get("port")
base_url = "http://{0}:{1}".format(host,port)

def get_data(url,k,d):
    try:
        resp = requests.get(url, timeout=5)
    except Exception as get_err:
        logger.error(str(get_err))
        return d
    if resp.status_code == 200:
        try:
            resp = resp.json()
        except Exception as to_json_err:
            logger.error(str(to_json_err))
            return d
        logger.info(str(resp))
        d[k] = resp
        if d.get("err_msg") is not None:
            d.pop("err_msg")
        return d

class Health(Resource):
    def get(self):
        if is_active == True:
            data = dict(err_msg="system error.")
            health_api = "/_cluster/health"
            health_url = base_url + health_api
            d = get_data(health_url,"cluster_health",data)
            return d

class NodeStatus(Resource):
    def get(self):
        if is_active == True:
            data = dict(err_msg="system error.")
            health_api = "/_nodes/stats"
            health_url = base_url + health_api
            d = get_data(health_url,"node_status",data)
            return d
