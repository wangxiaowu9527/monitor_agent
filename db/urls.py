from db import db_blue
from flask_restful import Api
from db.mysql.views import Base,SlaveStatus,MysqlLock,SlowQuery
from db.my_redis.views import Info,Latency

db_api = Api(db_blue)

# MySQL
db_api.add_resource(Base,"/mysql/base")
db_api.add_resource(SlaveStatus,"/mysql/slave_status")
db_api.add_resource(MysqlLock,"/mysql/lock")
db_api.add_resource(SlowQuery,"/mysql/slow_query")

# Redis
db_api.add_resource(Info,"/redis/info")
db_api.add_resource(Latency,"/redis/latency")


