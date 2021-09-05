from utils import logger
import config
import re

def _is_in_range_int(min:int,max:int,n:int,k=None):
    if isinstance(n,int):
        if min <= n <= max:
            return True
    if k:
        err_msg = "{0}: value must between {1} and {2},type int.".format(k, min, max)
        logger.error(err_msg)

def _is_in_list(l:list,p,k=None):
    if p in l:
        return True
    if k:
        err_msg = "{0}: value must in {1}.".format(k,l)
        logger.error(err_msg)

def _is_ip(ip,k=None):
    # not perfect
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip) or (ip == "localhost"):
        return True
    if k:
        err_msg = "{0}: value is invalid.".format(k)
        logger.error(err_msg)

def app_run_info():
    counter = 0
    counter_total = 17
    actives = [True,False]
    d = {
        "config.DEBUG": config.DEBUG,
        "config.node_base.os_base.is_active": config.node_base.get("os_base").get("is_active"),
        "config.node_base.cpu.is_active": config.node_base.get("cpu").get("is_active"),
        "config.node_base.mem.is_active": config.node_base.get("mem").get("is_active"),
        "config.node_base.net.is_active": config.node_base.get("net").get("is_active"),
        "config.db.mysql.is_active": config.db.get("mysql").get("is_active"),
        "config.db.redis.is_active": config.db.get("redis").get("is_active"),
        "config.docker.is_active": config.docker.get("is_active"),
        "config.k8s.is_active": config.k8s.get("is_active"),
        "config.middleware.rabbitmq.is_active": config.middleware.get("rabbitmq").get("is_active"),
        "config.middleware.elasticsearch.is_active": config.middleware.get("elasticsearch").get("is_active"),
        "config.middleware.zookeeper.is_active": config.middleware.get("zookeeper").get("is_active"),
        "config.middleware.kafka.is_active": config.middleware.get("kafka").get("is_active"),
        "config.middleware.jvm.is_active": config.middleware.get("jvm").get("is_active"),
        "config.middleware.nginx.is_active": config.middleware.get("nginx").get("is_active"),
    }
    for key,value in d.items():
        if _is_in_list(actives,value,k=key):
            counter += 1
    if _is_ip(config.RUN_HOST,k="config.RUN_HOST"):
        counter += 1
    if _is_in_range_int(1,65535,config.RUN_PORT,k="config.RUN_PORT"):
        counter += 1
    if counter == counter_total:
        return True

