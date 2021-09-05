from flask_restful import Resource
import psutil
from config import node_base
import platform
import os
import time

is_active = node_base.get("disk").get("is_active")

def linux_df(cmd,disk_type):
    dfs = os.popen(cmd).read()
    if dfs:
        dfs = dfs.split("\n")[1:]
        disks = list()
        for df in dfs:
            if df:
                disk = dict()
                disk["total"] = df.split()[1] if disk_type == "inode" else (int(df.split()[1])) * 1024
                disk["used"] = df.split()[2] if disk_type == "inode" else (int(df.split()[2])) * 1024
                disk["free"] = df.split()[3] if disk_type == "inode" else (int(df.split()[3])) * 1024
                disk["used_percent"] = df.split()[4]
                disk["mount_point"] = df.split()[5]
                disks.append(disk)

        return disks

class DiskDf(Resource):
    # unit: byte
    def get(self):
        if is_active == True:
            sys_type = platform.platform()
            if sys_type.startswith("Windows"):
                # windows: only block
                parts = psutil.disk_partitions()
                if parts:
                    mountpoints = list()
                    for part in parts:
                        if part:
                            mountpoint = part.mountpoint
                            mountpoints.append(mountpoint)
                    if mountpoints:
                        disks = list()
                        for mountpoint in mountpoints:
                            usage = psutil.disk_usage(mountpoint)
                            total = usage.total
                            used = usage.used
                            free = usage.free
                            used_percent = usage.percent
                            disk = {
                                "total": total,
                                "used": used,
                                "free": free,
                                "used_percent": used_percent,
                                "mount_point": mountpoint,
                            }
                            disks.append(disk)

                        data = {"block":disks}
                        return data

            if sys_type.startswith("Linux"):
                # linux: inode and block
                # inode unit: count ，block default unit: KB,need convert to byte
                inode_type = "inode"
                inode_cmd = "df -i"
                block_type = "block"
                block_cmd = "df"
                inode_disks = linux_df(inode_cmd,inode_type)
                block_disks = linux_df(block_cmd,block_type)
                data = {
                    block_type:block_disks,
                    inode_type:inode_disks,
                }
                return data

class DiskIO(Resource):
    # unit：Bytes/s
    def get(self):
        if is_active == True:
            d1 = psutil.disk_io_counters(perdisk=True)
            time.sleep(1)
            d2 = psutil.disk_io_counters(perdisk=True)
            data = dict()
            if d1:
                for k1,v1 in d1.items():
                    for k2,v2 in d2.items():
                        if k1 == k2:
                            read_bytes = v2.read_bytes - v1.read_bytes
                            write_bytes = v2.write_bytes - v1.write_bytes
                            data[k1] = dict(
                                rate_read_bytes=read_bytes,
                                rate_write_bytes=write_bytes
                            )
                return data
