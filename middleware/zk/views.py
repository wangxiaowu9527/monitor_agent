from flask_restful import Resource
from config import middleware
from utils import logger
import subprocess

zk = middleware.get("zookeeper")
is_active = zk.get("is_active")
host = zk.get("zk_host")
port = zk.get("zk_port")


def _check_param(host,port):
    if all([host,port]):
        return True

class Ruok(Resource):
    def get(self):
        if is_active == True:
            data = dict(err_msg="system error.")
            if _check_param(host,port):
                letter = "ruok"
                letter_cmd = "echo {0} | nc {1} {2}".format(letter,host,port)
                try:
                    ruok_res = subprocess.Popen(letter_cmd,
                                                   shell=True,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   close_fds=True)
                    cmd_out = ruok_res.stdout.readlines()
                    cmd_err = ruok_res.stderr.readlines()
                    if cmd_err:
                        for i in cmd_err:
                            try:
                                cmd_err_str = str(i)
                                logger.error(cmd_err_str)
                            except Exception as msg_to_str_err:
                                logger.error(str(msg_to_str_err))
                        return data
                    if cmd_out:
                        cmd_out = cmd_out[0]
                        try:
                            cmd_out_str = str(cmd_out, encoding="utf8")
                        except Exception as byte_to_str_err:
                            byte_to_str_err_msg = "byte to str failed.detail is:"
                            logger.error(byte_to_str_err_msg)
                            logger.error(str(byte_to_str_err))
                            return data
                        if cmd_out_str:
                            data["ruok"] = cmd_out_str
                            data.pop("err_msg")
                            return data
                    else:
                        data["ruok"] = "none"
                        data.pop("err_msg")
                        return data

                except Exception as letter_err:
                    logger.error(str(letter_err))
                    return data

            else:
                param_miss_err_msg = "params about zookeeper in config.py missed,check it first."
                logger.error(param_miss_err_msg)
                return data

class Mntr(Resource):
    def get(self):
        if is_active == True:
            data = dict(err_msg="system error.")
            if _check_param(host,port):
                letter = "mntr"
                letter_cmd = "echo {0} | nc {1} {2}".format(letter,host,port)
                try:
                    mntr_res = subprocess.Popen(letter_cmd,
                                                   shell=True,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   close_fds=True)
                    cmd_out = mntr_res.stdout.readlines()
                    cmd_err = mntr_res.stderr.readlines()
                    if cmd_err:
                        for i in cmd_err:
                            try:
                                cmd_err_str = str(i)
                                logger.error(cmd_err_str)
                            except Exception as msg_to_str_err:
                                logger.error(str(msg_to_str_err))
                        return data
                    if cmd_out:
                        logger.info(str(cmd_out))
                        for item in cmd_out:
                            if item:
                                try:
                                    item = str(item,encoding="utf8")
                                except Exception as byte_to_str_err:
                                    byte_to_str_err_msg = "byte to str failed.detail is:"
                                    logger.error(byte_to_str_err_msg)
                                    logger.error(str(byte_to_str_err))
                                    return data
                                item = item.split("\n")[0]
                                k = item.split("\t")[0]
                                v = item.split("\t")[1]
                                data[k] = v
                        data.pop("err_msg")
                        return data

                except Exception as mntr_err:
                    logger.error(str(mntr_err))
                    return data

            else:
                param_miss_err_msg = "params about zookeeper in config.py missed,check it first."
                logger.error(param_miss_err_msg)
                return data
