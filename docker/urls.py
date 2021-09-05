from docker import docker_blue
from flask_restful import Api
from docker.views import Stats,PsA

docker_api = Api(docker_blue)

docker_api.add_resource(Stats,"/stats")
docker_api.add_resource(PsA,"/ps_a")