from flask_restful import Resource
from config import k8s
from utils import logger
from kubernetes import client, config
import os

is_active = k8s.get("is_active")
conf = k8s.get("kube_config")

def is_exist(f):
    if f:
        if os.path.isfile(f):
            return True
        err_msg = "config.k8s.kube_config:{0} doesn't exist.".format(f)
        logger.error(err_msg)

class Nodes(Resource):
    def get(self):
        if is_active == True:
            if is_exist(conf):
                data = dict(msg="system error.")
                try:
                    config.kube_config.load_kube_config(config_file=conf)
                    api = client.CoreV1Api()
                except Exception as get_api_err:
                    logger.error(str(get_api_err))
                    return data
                try:
                    nodes = api.list_node()
                except Exception as node_err:
                    logger.error(str(node_err))
                    return data
                if nodes:
                    for i in nodes.items:
                        data[i.metadata.name] = {"name": i.metadata.name,
                                                 "status": i.status.conditions[-1].type if i.status.conditions[-1].status == "True" else "NotReady",
                                                 "ip": i.status.addresses[0].address,
                                                 "kubelet_version": i.status.node_info.kubelet_version,
                                                 "os_image": i.status.node_info.os_image,
                                                 }
                    if data.get("msg"):
                        data.pop("msg")
                    return data

class Pods(Resource):
    def get(self):
        if is_active == True:
            if is_exist(conf):
                data = dict(msg="system error.")
                try:
                    config.kube_config.load_kube_config(config_file=conf)
                    api = client.CoreV1Api()
                except Exception as get_api_err:
                    logger.error(str(get_api_err))
                    return data
                try:
                    pods = api.list_pod_for_all_namespaces()
                except Exception as pod_err:
                    logger.error(str(pod_err))
                    return data
                if pods:
                    for i in pods.items:
                        containers = list()
                        for container in i.status.container_statuses:
                            simple_pod = {
                                "container_name": container.name,
                                "ready": container.ready,
                                "restart_count": container.restart_count
                            }
                            containers.append(simple_pod)

                        data[i.metadata.name] = {
                            "ip": i.status.pod_ip,
                            "namespace": i.metadata.namespace,
                            "node_name": i.spec.node_name,
                            "containers": containers
                        }
                    if data.get("msg"):
                        data.pop("msg")
                    return data
