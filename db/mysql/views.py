from flask_restful import Resource
from config import db
import pymysql
from utils import logger
import time

mysql_info = db.get("mysql")
is_active = mysql_info.get("is_active")

def alive():
    host = mysql_info.get("host")
    user = mysql_info.get("user")
    password = mysql_info.get("password")
    port = mysql_info.get("port")
    if all([host,user,password,port]):
        try:
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                # db='information_schema',
                charset='utf8'
            )
        except Exception as conn_err:
            conn_err_msg = "connect to mysql failed, detail is following:"
            logger.error(conn_err_msg)
            logger.error(str(conn_err))
            return

        return {"conn":conn}

    else:
        mysql_info_not_enough_msg = "mysql info is not enough in config.py ,check it."
        logger.error(mysql_info_not_enough_msg)
        return

# base items: is_alive | version | QPS | TPS | client_connected_percent | buffer_pool_percent and so on
class Base(Resource):
    def get(self):
        if is_active == True:
            data = dict()
            is_alive = alive()
            if is_alive:
                data["is_alive"] = True
                conn = is_alive.get("conn")
                cur = conn.cursor()

                # get single result by SQL
                def get_sql_res(sql):
                    cur.execute(sql)
                    res = cur.fetchone()
                    if res:
                        sql_res = str(res[-1])
                        return sql_res

                # get multi result by SQL
                def get_sql_all_res(sql):
                    cur.execute(sql)
                    res = cur.fetchall()
                    if res:
                        res_d = dict()
                        for t in res:
                            if t:
                                res_d[t[0]] = t[1]
                        return res_d

                # QPS: requests every second
                qps_sql = "show global status " \
                          "where variable_name in " \
                          "('Queries', 'Uptime')"
                qps_sql_res_first = get_sql_all_res(qps_sql)
                # time.sleep(1)
                # qps_sql_res_second = get_sql_all_res(qps_sql)
                if qps_sql_res_first: #and qps_sql_res_second:
                    try:
                        qps_first_queries = int(qps_sql_res_first.get("Queries"))
                        qps_first_uptime = int(qps_sql_res_first.get("Uptime"))
                        # qps_second_queries = int(qps_sql_res_second.get("Queries"))
                        # qps_second_uptime = int(qps_sql_res_second.get("Uptime"))
                        # qps = (qps_second_queries - qps_first_queries)/(qps_second_uptime - qps_first_uptime)
                        data["qps"] = {
                            "queries_total": qps_first_queries,
                            "uptime_total": qps_first_uptime
                        }
                    except Exception as qps_err:
                        logger.error(str(qps_err))

                # TPS：number of transactions processed per second
                tps_sql = "show global status " \
                          "where variable_name in " \
                          "('Com_insert' , " \
                          "'Com_delete' , " \
                          "'Com_update'," \
                          "'Com_select', " \
                          "'Uptime')"
                tps_sql_res_first = get_sql_all_res(tps_sql)
                # time.sleep(1)
                # tps_sql_res_second = get_sql_all_res(tps_sql)
                if tps_sql_res_first: #and tps_sql_res_second:
                    try:
                        # logger.info("tps_first:" + str(tps_sql_res_first))
                        # logger.info("tps_second:" + str(tps_sql_res_second))
                        tps_first_uptime = int(tps_sql_res_first.get("Uptime"))
                        # tps_second_uptime = int(tps_sql_res_second.get("Uptime"))
                        tps_first_insert = int(tps_sql_res_first.get("Com_insert"))
                        # tps_second_insert = int(tps_sql_res_second.get("Com_insert"))
                        # tps_insert = (tps_second_insert - tps_first_insert)/(tps_second_uptime -tps_first_uptime)
                        tps_first_delete = int(tps_sql_res_first.get("Com_delete"))
                        # tps_second_delete = int(tps_sql_res_second.get("Com_delete"))
                        # tps_delete = (tps_second_delete - tps_first_delete) / (tps_second_uptime - tps_first_uptime)
                        tps_first_update = int(tps_sql_res_first.get("Com_update"))
                        # tps_second_update = int(tps_sql_res_second.get("Com_update"))
                        # tps_update = (tps_second_update - tps_first_update) / (tps_second_uptime - tps_first_uptime)
                        # data["tps_update"] = tps_update
                        tps_first_select = int(tps_sql_res_first.get("Com_select"))
                        # tps_second_select = int(tps_sql_res_second.get("Com_select"))
                        # tps_select = (tps_second_select - tps_first_select) / (tps_second_uptime - tps_first_uptime)
                        # data["tps_select"] = tps_select
                        data["tps"] = {
                            "insert_total": tps_first_insert,
                            "delete_total": tps_first_delete,
                            "update_total": tps_first_update,
                            "select_total": tps_first_select,
                            "uptime_total": tps_first_uptime
                        }
                    except Exception as tps_err:
                        logger.error(str(tps_err))

                # version
                version_sql = "select version()"
                version_sql_res = get_sql_res(version_sql)
                if version_sql_res:
                    data["version"] = version_sql_res

                # max connections
                max_conn_sql = "show global variables like 'max_connections'"
                max_conn_sql_res = get_sql_res(max_conn_sql)
                if max_conn_sql_res:
                    data["max_connections"] = max_conn_sql_res

                #current connections
                threads_connected_sql = "show global status like 'Threads_connected'"
                threads_connected_sql_res = get_sql_res(threads_connected_sql)
                if threads_connected_sql_res:
                    data["threads_connected"] = threads_connected_sql_res

                # connection_used_percent
                if max_conn_sql_res and threads_connected_sql_res:
                    max_conn_sql_res = int(max_conn_sql_res)
                    threads_connected_sql_res = int(threads_connected_sql_res)
                    try:
                        threads_connected_percent = threads_connected_sql_res/max_conn_sql_res
                        threads_connected_percent = str(threads_connected_percent)[:6]
                        # logger.info(threads_connected_percent)
                        data["threads_connected_percent"] = threads_connected_percent
                    except Exception as threads_connected_percent_err:
                        logger.error(str(threads_connected_percent_err))

                # thread running numbers
                threads_running_sql = "show global status like 'Threads_running'"
                threads_running_sql_res = get_sql_res(threads_running_sql)
                if threads_running_sql_res:
                    data["threads_running"] = threads_running_sql_res

                # innodb_buffer_pool_read_percent
                innodb_buffer_pool_read_requests_sql = "show global status like 'innodb_buffer_pool_read_requests'"
                innodb_buffer_pool_read_requests_res = get_sql_res(innodb_buffer_pool_read_requests_sql)
                innodb_buffer_pool_reads_sql = "show global status like 'innodb_buffer_pool_reads'"
                innodb_buffer_pool_reads_res = get_sql_res(innodb_buffer_pool_reads_sql)
                if str(innodb_buffer_pool_read_requests_res) and str(innodb_buffer_pool_reads_res):
                    try:
                        innodb_buffer_pool_read_percent = (int(innodb_buffer_pool_read_requests_res) - int(innodb_buffer_pool_reads_res))/int(innodb_buffer_pool_read_requests_res)
                        innodb_buffer_pool_read_percent = str(innodb_buffer_pool_read_percent)[:6]
                        data["innodb_buffer_pool_read_requests"] = innodb_buffer_pool_read_requests_res
                        data["innodb_buffer_pool_reads"] = innodb_buffer_pool_reads_res
                        data["innodb_buffer_pool_read_percent"] = innodb_buffer_pool_read_percent
                    except Exception as innodb_buffer_pool_read_percent_err:
                        logger.error(str(innodb_buffer_pool_read_percent_err))

                cur.close()
                conn.close()

            else:
                data["is_alive"] = False

            return data

# slave status
class SlaveStatus(Resource):
    def get(self):
        # method 1: query by SQL
        '''
        three metrics：
        1、Slave_IO_Running == Yes and Slave_SQL_Running == Yes
        2、Master_Log_File == Relay_Master_Log_File
        3、Read_Master_Log_Pos - Exec_Master_Log_Pos > 10000 (value can be self defined)
        '''
        is_slave = mysql_info.get("is_slave")
        if is_active == True and is_slave == True:
            data = dict()
            is_alive = alive()
            if is_alive:
                conn = is_alive.get("conn")
                cur = conn.cursor()
                slave_status_sql = "show slave status"
                try:
                    cur.execute(slave_status_sql)
                    slave_res = cur.fetchone()
                    if slave_res:
                        slave_io_running = slave_res[10]
                        slave_sql_running = slave_res[11]
                        master_log_file = slave_res[5]
                        relay_master_log_file = slave_res[9]
                        read_master_log_pos = slave_res[6]
                        exec_master_log_pos = slave_res[21]
                        master_log_pos_diff = int(read_master_log_pos) - int(exec_master_log_pos)
                        data["slave_io_running"] = slave_io_running
                        data["slave_sql_running"] = slave_sql_running
                        data["master_log_file"] = master_log_file
                        data["relay_master_log_file"] = relay_master_log_file
                        data["read_master_log_pos"] = read_master_log_pos
                        data["exec_master_log_pos"] = exec_master_log_pos
                        data["master_log_pos_diff"] = master_log_pos_diff

                    else:
                        data["slave_status"] = "empty"
                except Exception as exe_err:
                    err_msg = "execute sql: {0} failed,detail is:".format(slave_status_sql)
                    logger.error(err_msg)
                    logger.error(str(exe_err))
                    data["slave_status"] = "sys_err"
                finally:
                    cur.close()
                    conn.close()
            else:
                data["is_alive"] = False
            return data

        # method 2: use pt-heartbeat , ignore this moment

# TODO slow query
class SlowQuery(Resource):
    def get(self):
        # 1 query from slow_query_log directly
        '''
        method：
        1、confirm whether the slow query switch has been turned on first：
        mysql> show variables like 'slow_query%';  【value must be: ON】
            +---------------------------+----------------------------------+
            | Variable_name             | Value                            |
            +---------------------------+----------------------------------+
            | slow_query_log            | OFF                              |
            | slow_query_log_file       | /mysql/data/localhost-slow.log   |
            +---------------------------+----------------------------------+

            mysql> show variables like 'long_query_time'; 【default limit value：10 seconds】
            +-----------------+-----------+
            | Variable_name   | Value     |
            +-----------------+-----------+
            | long_query_time | 10.000000 |
            +-----------------+-----------+
        2、confirm work is ok，then get the key words（such as: select sleep(15) to test）,
           the following is an example:
           root@localhost:/var/lib/mysql# cat localhost-slow.log

            mysqld, Version: 5.7.32-log (MySQL Community Server (GPL)). started with:
            Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock
            Time                 Id Command    Argument
            # Time: 2021-07-21T16:24:16.359923Z
            # User@Host: root[root] @ localhost []  Id:    22
            # Query_time: 12.188823  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 0
            SET timestamp=1626884656;
            select sleep(12);
            # Time: 2021-07-21T16:25:29.541402Z
            # User@Host: root[root] @ localhost []  Id:    22
            # Query_time: 13.046798  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 0
            SET timestamp=1626884729;
        '''

        # 2 The SQL statement is only suitable for real-time troubleshooting (because you can't find it after SQL execution)
        '''
        slow_query_sql = "SELECT DISTINCT * FROM information_schema.PROCESSLIST " \
                         "WHERE COMMAND = 'Query' " \
                         "AND TIME > 10 ORDER BY TIME DESC LIMIT 20"
        '''
        pass

# TODO about lock
class MysqlLock(Resource):
    def get(self):
        '''
        SELECT
        b.trx_mysql_thread_id AS 'blocked_thread_id', # blocked_id
        b.trx_query AS 'blocked_sql_text', # blocked_SQL
        c.trx_mysql_thread_id AS 'blocker_thread_id', # blocker_id
        c.trx_query AS 'blocker_sql_text', # blocker_SQL
        ( Unix_timestamp() - Unix_timestamp(c.trx_started) ) AS 'blocked_time'  # block_time
        FROM   information_schema.innodb_lock_waits a
        INNER JOIN information_schema.innodb_trx b
        ON a.requesting_trx_id = b.trx_id
        INNER JOIN information_schema.innodb_trx c
        ON a.blocking_trx_id = c.trx_id
        WHERE  ( Unix_timestamp() - Unix_timestamp(c.trx_started) ) > 30;
        '''
        pass
