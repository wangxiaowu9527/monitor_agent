from middleware import middleware_blue
from flask_restful import Api
from middleware.rabbitmq.views import Nodes,Msgs
from middleware.elastic.views import Health,NodeStatus
from middleware.jvm.views import Heap,GC
from middleware.nginx.views import IsAlive,AccessLog
from middleware.zk.views import Ruok,Mntr
from middleware.kafka.views import KafkaJMX

middleware_api = Api(middleware_blue)

# Rabbitmq
middleware_api.add_resource(Nodes,"/rabbitmq/nodes")
middleware_api.add_resource(Msgs,"/rabbitmq/msgs")

# Elastic
middleware_api.add_resource(Health,"/elastic/health")
middleware_api.add_resource(NodeStatus,"/elastic/node_status")

# JVM
middleware_api.add_resource(Heap,"/jvm/heap")
middleware_api.add_resource(GC,"/jvm/gc")

# Nginx
middleware_api.add_resource(IsAlive,"/nginx/is_alive")
middleware_api.add_resource(AccessLog,"/nginx/access_log")

# Zookeeper
middleware_api.add_resource(Ruok,"/zk/ruok")
middleware_api.add_resource(Mntr,"/zk/mntr")

# Kafka
middleware_api.add_resource(KafkaJMX,"/kafka/jmx")