import subprocess
from flask_restful import Resource
from config import db
from utils import logger
from redis import Redis

redis_info = db.get("redis")
is_active = redis_info.get("is_active")
redis_host = redis_info.get("host")
redis_port = redis_info.get("port")
redis_password = redis_info.get("password")

def alive():
    if all([redis_host,redis_port,redis_password]):
        r = Redis(
            host=redis_host,
            password=redis_password,
            port=redis_port,
            socket_timeout=5,
            socket_connect_timeout=5
        )
        try:
            r_ping = r.ping() # True or False
            if r_ping:
                return r
        except Exception as ping_err:
            ping_err_msg = "execute redis cmd: [ping] failed,detail is:"
            logger.error(ping_err_msg)
            logger.error(str(ping_err))
            return

    redis_info_not_enough_msg = "redis info is not enough in config.py ,check it."
    logger.error(redis_info_not_enough_msg)
    return

class Info(Resource):
    def get(self):
        if is_active == True:
            data = dict()
            r = alive()
            if r:
                data["is_alive"] = True
                # all_conf = r.config_get("*") => get all config info
                # max_clients = r.config_get("maxclients")
                info = r.info()
                data["info"] = info
                r.close()
            else:
                data["is_alive"] = False
            return data

class Latency(Resource):
    def get(self):
        if is_active == True:
            data = dict(err_msg="system error.")
            latency_cmd = "redis-cli --latency -h {0} -p {1} -a {2}".format(redis_host,
                                                                            redis_port,
                                                                            redis_password
                                                                            )
            try:
                latency_res = subprocess.Popen(latency_cmd,
                                               shell=True,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               close_fds=True)
                cmd_out = latency_res.stdout.readlines()
                cmd_err = latency_res.stderr.readlines()
                if cmd_err:
                    for i in cmd_err:
                        try:
                            cmd_err_str = str(i)
                            logger.error(cmd_err_str)
                        except Exception as msg_to_str_err:
                            logger.error(str(msg_to_str_err))
                if cmd_out:
                    cmd_out = cmd_out[0]
                    try:
                        cmd_out_str = str(cmd_out,encoding="utf8")
                    except Exception as byte_to_str_err:
                        byte_to_str_err_msg = "byte to str failed.detail is:"
                        logger.error(byte_to_str_err_msg)
                        logger.error(str(byte_to_str_err))
                        return data
                    if cmd_out_str:
                        cmd_out_str_list = cmd_out_str.split()
                        min = cmd_out_str_list[0]
                        max = cmd_out_str_list[1]
                        avg = cmd_out_str_list[2]
                        data["min"] = min
                        data["max"] = max
                        data["avg"] = avg
                        data.pop("err_msg")
                        return data

            except Exception as latency_err:
                logger.error(str(latency_err))
                return data