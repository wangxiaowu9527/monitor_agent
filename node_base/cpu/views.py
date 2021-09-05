from flask_restful import Resource
import psutil
import platform
from config import node_base
from utils import logger
from utils.check_conf import _is_in_range_int

class CPU(Resource):
    def get(self):
        is_active = node_base.get("cpu").get("is_active")
        if is_active == True:
            # check interval if between 1 and 10
            interval = node_base.get("cpu").get("interval")
            if not _is_in_range_int(1,10,interval,k="config.node_base.cpu.interval"):
                return
            # cpu_count
            real_num = psutil.cpu_count(logical=False)
            logic_num = psutil.cpu_count(logical=True)
            # cpu_used_percent
            total_used_percent = psutil.cpu_percent(interval=interval)
            sys_type = platform.platform()
            if sys_type.startswith("Linux"):
                # load_average
                loadavg = psutil.getloadavg()
                loadavg_1 = loadavg[0]
                loadavg_5 = loadavg[1]
                loadavg_15 = loadavg[2]
                # io about
                io_percent = psutil.cpu_times_percent()
                user_percent = io_percent.user
                sys_percent = io_percent.system
                idle_percent = io_percent.idle
                wait_percent = io_percent.iowait

                data = {
                    "real_num": real_num,
                    "logic_num": logic_num,
                    "total_used_percent": total_used_percent,
                    "user_percent":user_percent,
                    "sys_percent":sys_percent,
                    "idle_percent":idle_percent,
                    "wait_percent":wait_percent,
                    "loadavg_1":loadavg_1,
                    "loadavg_5": loadavg_5,
                    "loadavg_15": loadavg_15,
                }
                return data

            if sys_type.startswith("Windows"):
                data = {
                    "real_num":real_num,
                    "logic_num":logic_num,
                    "total_used_percent":total_used_percent,
                }
                return data



