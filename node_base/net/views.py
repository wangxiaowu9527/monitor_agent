from flask_restful import Resource
import psutil
import time
from config import node_base

class NetIO(Resource):
    def get(self):
        is_active = node_base.get("net").get("is_active")
        if is_active == True:
            n1 = psutil.net_io_counters(pernic=True)
            time.sleep(1)
            n2 = psutil.net_io_counters(pernic=True)
            if n1:
                data = dict()
                for k1,v1 in n1.items():
                    for k2,v2 in n2.items():
                        if k1 == k2:
                            net_in = v2.bytes_recv - v1.bytes_recv
                            net_out = v2.bytes_sent - v1.bytes_sent
                            err_in = v2.errin -v1.errin
                            err_out = v2.errout -v1.errout
                            drop_in = v2.dropin - v1.dropin
                            drop_out = v2.dropout - v1.dropout
                            data[k1] = dict(
                                rate_net_in_bytes=net_in,
                                rate_net_out_bytes=net_out,
                                err_in_total=err_in,
                                err_out_total=err_out,
                                drop_in_total=drop_in,
                                drop_out_total=drop_out
                            )
                return data
