########## Base Run Info ###########

DEBUG = False
RUN_HOST = "0.0.0.0"
RUN_PORT = 52013
LOG_NAME = "out.log"
LOG_LEVEL = "INFO"

###########  Monitor Items ##########

# NodeBase
node_base = {

    "os_base": {"is_active":True},

    "cpu": {
        "is_active":True,
        "interval": 1   # between 1~10
    },

    "mem": {"is_active":True},

    "disk": {"is_active":True},

    "net": {"is_active":True},

}

# DataBase
db = {

    "mysql": {
        "is_active": False,
        "host": "localhost",
        "user": "user1",
        "password": "123456",
        "port": 3306,
        "is_slave": True,
    },

    "redis":{
        "is_active": False,
        "host": "localhost",
        "password": "123456",
        "port": 6379,
    }

}

# Docker (Need on Node Host)
docker = {"is_active": False}

# K8S
k8s = {
    "is_active": False,
    # download from k8s cluster that can execute command: kubectl,source default path: ~/.kube/config
    "kube_config": "D:\py_projects\monitor_agent\k8s\config.yaml"
}

# Middleware
middleware = {
    # need enable management
    "rabbitmq":{
        "is_active": False,
        "user": "user1",  # make sure this user's tag is monitoring in rabbitmq
        "password": "123456",
        "host": "localhost",
        "manage_port": 15672,
    },

    "elasticsearch":{
        "is_active": False,
        "host": "localhost",
        "port": 9200,
    },

    # TODO
    "jvm":{
        "is_active": False,
    },

    # TODO
    "nginx":{
        "is_active": False,
    },

    "kafka":{
        "is_active": False,
        "kafka_host":"localhost",
        "kafka_jmx_port": 8888  # make sure the kafka_server enabled JMX_PORT before start
    },

    "zookeeper":{
        "is_active": False,
        "zk_host": "localhost",
        "zk_port": 2181
    },
}


