from flask_restful import Resource
from config import node_base
import socket
import platform

class OsBase(Resource):
    def get(self):
        is_active = node_base.get("os_base").get("is_active")
        if is_active == True:
            hostname = socket.gethostname()
            ip_main = socket.gethostbyname(hostname)
            sys_type = platform.platform()
            data = {
                "hostname":hostname,
                "ip_main":ip_main,
                "sys_type":sys_type,
            }
            return data

