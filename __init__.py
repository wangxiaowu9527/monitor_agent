from flask import Flask
from node_base import node_base_blue
from db import db_blue
from docker import docker_blue
from middleware import middleware_blue
from k8s import k8s_blue

def create_app():
    app = Flask(__name__)
    # registry blueprint
    app.register_blueprint(node_base_blue,url_prefix="/node_base")
    app.register_blueprint(db_blue,url_prefix="/db")
    app.register_blueprint(docker_blue,url_prefix="/docker")
    app.register_blueprint(middleware_blue,url_prefix="/middleware")
    app.register_blueprint(k8s_blue,url_prefix="/k8s")
    return app

app = create_app()

from utils.check_conf import app_run_info
from utils import logger

if app_run_info():
    logger.info("url_maps:")
    logger.info(str(app.url_map))
else:
    exit(1)

