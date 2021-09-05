import logging
from utils.handlers import MidnightRotatingFileHandler
import sys
import os
from config import LOG_LEVEL,LOG_NAME


# write logs to ${base_dir}/logs/out.log and split by day
current_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(current_path)
log_dir = os.path.join(base_path,"logs")
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)
log_name = os.path.join(log_dir,LOG_NAME)

def register_log():
    fmt = "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s - %(message)s"
    handler_file = MidnightRotatingFileHandler(log_name)   # to file
    handler_consule = logging.StreamHandler(sys.stdout)    # to console
    logging.basicConfig(
        level=logging.INFO, # global base level
        format=fmt,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[handler_file,handler_consule]
    )

    level_info = {
        "DEBUG":logging.DEBUG,
        "INFO":logging.INFO,
        "WARNING":logging.WARNING,
        "ERROR":logging.ERROR,
        "CRITICAL":logging.CRITICAL
    }

    logging.getLogger(__name__).setLevel(level_info.get(LOG_LEVEL))  # self defined log level

register_log()
logger = logging.getLogger(__name__)



