from flask_restful import Resource
from config import middleware
from utils import logger
from jmxquery import JMXConnection, JMXQuery

kafka = middleware.get("kafka")
is_active = kafka.get("is_active")
host = kafka.get("kafka_host")
jmx_port = kafka.get("kafka_jmx_port")

class KafkaJMX(Resource):
    def get(self):
        if is_active == True:
            data = dict(err_msg="system error.")
            if not all([host,jmx_port]):
                param_missing_msg = "make sure the params about kafka in config.py are set first."
                logger.error(param_missing_msg)
                return data

            jmx_url = "service:jmx:rmi:///jndi/rmi://{0}:{1}/jmxrmi".format(host,jmx_port)
            jmxConnection = JMXConnection(jmx_url)
            jmxQuery = [JMXQuery("*:*")]
            try:
                metrics = jmxConnection.query(jmxQuery)
            except FileNotFoundError:
                no_java_msg = "make sure the cmd: java is in $PATH first!"
                logger.error(no_java_msg)
                return data
            except Exception as other_err:
                logger.error(str(other_err))
                return data
            if metrics:
                jmxs = list()
                for metric in metrics:
                    jmx = dict()
                    # print(f"{metric.to_query_string()} ({metric.value_type}) = {metric.value}")
                    metric_str = metric.to_query_string()
                    metric_val = metric.value
                    logger.info(str(metric_str) + ":" + str(metric_val))
                    jmx["metric_str"] = metric_str
                    jmx["metric_val"] = metric_val
                    jmxs.append(jmx)
                data["jmxs"] = jmxs
                data.pop("err_msg")
                return data
