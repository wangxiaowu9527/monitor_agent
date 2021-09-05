from flask_restful import Resource
from config import middleware
from utils import logger
import requests
from multiprocessing import Pool

mq = middleware.get("rabbitmq")
is_active = mq.get("is_active")
user = mq.get("user")
password = mq.get("password")
host = mq.get("host")
manage_port = mq.get("manage_port")
manage_base_url = "http://{0}:{1}".format(host,manage_port)

class Nodes(Resource):
    def get(self):
        if is_active == True:
            data = dict(err_msg="system error.")
            node_api = "/api/nodes"
            node_url = manage_base_url + node_api
            try:
                resp = requests.get(node_url,auth=(user,password),timeout=5)
            except Exception as get_node_api_err:
                logger.error(str(get_node_api_err))
                return data
            if resp.status_code == 200:
                try:
                    resp = resp.json()
                except Exception as to_json_err:
                    logger.error(str(to_json_err))
                    return data
                data["nodes"] = resp
                data.pop("err_msg")
                return data
            else:
                resp_text = str(resp.text)
                logger.error(resp_text)
                return data

class Msgs(Resource):
    def get(self):
        if is_active == True:
            data = dict(err_msg="system error.")
            # get all vhosts
            vhosts_api = "/api/vhosts"
            vhosts_url = manage_base_url + vhosts_api
            try:
                vhosts_resp = requests.get(vhosts_url,auth=(user,password),timeout=5)
            except Exception as get_vhosts_api_err:
                logger.error(str(get_vhosts_api_err))
                return data
            if vhosts_resp.status_code == 200:
                try:
                    vhosts_resp = vhosts_resp.json()
                except Exception as vhosts_resp_to_json_err:
                    logger.error(str(vhosts_resp_to_json_err))
                    return data
                logger.info(str(vhosts_resp))
                if vhosts_resp:
                    vhosts = list()
                    for vhost in vhosts_resp:
                        if vhost:
                            vhost_name = vhost.get("name")
                            if "/" in vhost_name:
                                vhost_name = vhost_name.replace("/","%2f")
                            vhosts.append(vhost_name)
                    logger.info("vhosts:" + str(vhosts))
                    if vhosts:
                        # get messages in each vhost with multiprocess
                        pool = Pool(5)
                        results = list()
                        for host in vhosts:
                            queue_res = pool.apply_async(self.vhost_msg,(host,))
                            results.append(queue_res)
                        pool.close()
                        pool.join()
                        if results:
                            msgs_data = list()
                            for r in results:
                                if r:
                                    g = r.get()
                                    if g:
                                        msgs_data.append(g)
                            return msgs_data


    def vhost_msg(self,vhost_name):
        queues_msg_api = "/api/queues/{0}".format(vhost_name)
        queues_msg_url = manage_base_url + queues_msg_api
        try:
            queues_resp = requests.get(queues_msg_url,auth=(user,password),timeout=5)
        except Exception as get_queues_api_err:
            logger.error(str(get_queues_api_err))
            return
        if queues_resp.status_code == 200:
            try:
                queues_resp = queues_resp.json()
            except Exception as queues_resp_to_json_err:
                logger.error(str(queues_resp_to_json_err))
                return
            if queues_resp:
                queues_list = list()
                for queue in queues_resp:
                    queue_data = dict()
                    queue_name = queue.get("name")
                    queue_vhost = queue.get("vhost")
                    queue_msg = queue.get("messages")
                    queue_data["queue_vhost"] = queue_vhost
                    queue_data["queue_name"] = queue_name
                    queue_data["queue_msg"] = queue_msg
                    queues_list.append(queue_data)
                return queues_list
