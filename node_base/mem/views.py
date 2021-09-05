from flask_restful import Resource
from config import node_base
import psutil

class Mem(Resource):
    # unit: byte
    def get(self):
        is_active = node_base.get("mem").get("is_active")
        if is_active == True:
            # physical memory
            virtual_mem = psutil.virtual_memory()
            virtual_mem_total = virtual_mem.total
            virtual_mem_used = virtual_mem.used
            virtual_mem_avail = virtual_mem.available
            virtual_mem_used_percent = virtual_mem.percent
            # swap memory
            swap_mem = psutil.swap_memory()
            swap_mem_total = swap_mem.total
            swap_mem_used = swap_mem.used
            swap_mem_avail = swap_mem_total - swap_mem_used
            swap_mem_used_percent = swap_mem.percent

            data = {
                "virtual":{
                    "total": virtual_mem_total,
                    "used": virtual_mem_used,
                    "available": virtual_mem_avail,
                    "used_percent": virtual_mem_used_percent,
                },
                "swap":{
                    "total": swap_mem_total,
                    "used": swap_mem_used,
                    "available": swap_mem_avail,
                    "used_percent": swap_mem_used_percent,
                }
            }

            return data


