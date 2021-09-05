from flask_restful import Resource
from config import docker
from utils import logger
import os
from multiprocessing import Pool


is_active = docker.get("is_active")
get_all_containers_cmd = "docker ps -a | awk '{print $NF}'"
get_running_containers_cmd = "docker ps | awk '{print $NF}'"

def alive():
    check_cmd = "docker ps"
    check_res = os.system(check_cmd)
    if check_res == 0:
        return True

# get container names by status
def containers(cmd):
    res = os.popen(cmd).read()
    if res:
        res = res.split("\n")
        if len(res) > 1:
            names = res[1:]
            container_names = list()
            for name in names:
                if name:
                    container_names.append(name)
            return container_names

# only get metrics of running containers
class Stats(Resource):
    def get(self):
        if is_active == True:
            is_alive = alive()
            run_data = dict()
            if is_alive == True:
                running_containers = containers(get_running_containers_cmd)
                if running_containers:
                    # with multiprocess
                    pool = Pool(5)
                    results = []
                    for container in running_containers:
                        info = pool.apply_async(self.used_info,(container,))
                        results.append(info)
                    pool.close()
                    pool.join()
                    if results: # objects of subprocess
                        stats_res = []
                        for r in results:
                            g = r.get() # real value in subprocess object
                            if g:
                                stats_res.append(g)
                        run_data["stats"] = str(stats_res)
            else:
                run_data["is_alive"] = False
            return run_data

    # about single container
    def used_info(self,container_name):
        cmd = "docker stats {0} --no-stream".format(container_name)
        cmd_res = os.popen(cmd).read()
        if cmd_res:
            cmd_res = cmd_res.split("\n")[1].split()
            data = dict()
            try:
                cpu_used_percent = cmd_res[2]
                mem_used = cmd_res[3]
                mem_limit = cmd_res[5]
                mem_used_percent = cmd_res[6]
                net_in = cmd_res[7]
                net_out = cmd_res[9]
                block_in = cmd_res[10]
                block_out = cmd_res[12]
                pids = cmd_res[-1]

            except Exception as used_info_err:
                err_msg = "get container used info failed,detail is:"
                logger.error(err_msg)
                logger.error(str(used_info_err))
                return

            data["container_name"] = container_name
            data["cpu_used_percent"] = cpu_used_percent
            data["mem_used"] = mem_used
            data["mem_limit"] = mem_limit
            data["mem_used_percent"] = mem_used_percent
            data["net_in"] = net_in
            data["net_out"] = net_out
            data["block_in"] =block_in
            data["block_out"] = block_out
            data["pids"] = pids

            return data

# command equals：docker ps -a
class PsA(Resource):
    def get(self):
        if is_active == True:
            is_alive = alive()
            data = dict()
            if is_alive == True:
                all_containers = containers(get_all_containers_cmd)
                running_containers = containers(get_running_containers_cmd)
                if all_containers:
                    exited_containers = list()
                    if running_containers:
                        data["running_containers"] = running_containers
                        for container in all_containers:
                            if container not in running_containers:
                                exited_containers.append(container)
                        data["exited_containers"] = exited_containers
                    else:
                        data["exited_containers"] = all_containers
            else:
                data["is_alive"] = False
            return data
