
项目简介：基于轻量级Flask开发的监控插件,Python版本:3.6.8，支持Windows、Linux部署
         包含了工作中常用的类型大部分监控指标，欢迎试用
使用方法：
（1）安装Python3环境
（2）下载代码，进入到项目目录下，执行：pip3 install -r requirements.txt
（3）启动：Linux系统执行 start_main.sh
         Windows系统执行 start_main.bat
         若不考虑性能，可直接执行 python3 main.py
---------------------------------------------------------------

1、设计思路：将监控项以接口形式暴露(json格式)，需求方直接发送GET请求即可 
2、在配置文件中设置了开关（config.py），基础资源模块设置了True，其它默认为False
   请按业务需要设置开关和参数，示例如下：

    "mysql": {
        "is_active": True,    # 启用开关
        "host": "localhost",  # MySQL的域名/IP
        "user": "root",       # 数据库用户名
        "password": "123456", # 数据库密码
        "port": 63306,        # 数据库端口
        "is_slave": False,    # 是否从库
    }

3、包含模块：
（1）基础资源：CPU、内存、磁盘、网络I/O等：需部署到每台节点
（2）数据库：MySQL、Redis等
（3）中间件：Kafka、RabbitMQ、Nginx、Elasticsearch、Zookeeper等
（4）Docker：需部署到宿主机
（5）K8S
 ......


