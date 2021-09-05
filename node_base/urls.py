from node_base import node_base_blue
from flask_restful import Api
from node_base.os_base.views import OsBase
from node_base.mem.views import Mem
from node_base.disk.views import DiskDf,DiskIO
from node_base.net.views import NetIO
from node_base.cpu.views import CPU

node_base_api = Api(node_base_blue)

# NodeBaseInfo
node_base_api.add_resource(OsBase,"/os_base")

# CPU
node_base_api.add_resource(CPU,"/cpu")

# Memory
node_base_api.add_resource(Mem,"/mem")

# Disk
node_base_api.add_resource(DiskDf,"/disk_df")
node_base_api.add_resource(DiskIO,"/disk_io")

# Net
node_base_api.add_resource(NetIO,"/net_io")
