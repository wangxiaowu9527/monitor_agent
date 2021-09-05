from k8s import k8s_blue
from flask_restful import Api
from k8s.views import Nodes,Pods

k8s_api = Api(k8s_blue)

# views
k8s_api.add_resource(Nodes,"/nodes")
k8s_api.add_resource(Pods,"/pods")
