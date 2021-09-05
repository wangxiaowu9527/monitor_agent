# The log file cannot be renamed on write due to multiple processes
# Rewriting method: write a log matching the date format of the current day,
# and soft link the main log file to it

import codecs
import datetime
import os
from logging.handlers import BaseRotatingHandler

class MidnightRotatingFileHandler(BaseRotatingHandler):
    def __init__(self, filename):
        self.suffix = "%Y-%m-%d"
        self.date = datetime.date.today()
        super(BaseRotatingHandler, self).__init__(filename, mode='a', encoding=None, delay=0)

    def shouldRollover(self, record):
        return self.date != datetime.date.today()

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.date = datetime.date.today()

    def _open(self):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("{0} - INFO - [log_name_latest_symlink]:".format(now_time), self.baseFilename)
        filename = '%s.%s' % (self.baseFilename, self.date.strftime(self.suffix))
        print("{0} - INFO - [log_name_latest]:".format(now_time),filename)
        if self.encoding is None:
            stream = open(filename, self.mode)
        else:
            stream = codecs.open(filename, self.mode, self.encoding)
        if os.path.exists(self.baseFilename):
            try:
                exist_msg = "{0} - INFO - {1} is already exists,removing it ...".format(now_time,self.baseFilename)
                print(exist_msg)
                os.remove(self.baseFilename)
            except OSError as del_log_symlink_error:
                print("{0} - ERROR - del_log_symlink_error:".format(now_time),del_log_symlink_error)
        try:
            print("{0} - INFO - symlink {1} to {2} ...".format(now_time,self.baseFilename,filename))
            os.symlink(filename, self.baseFilename)
        except OSError as create_log_symlink_err:
            print("{0} - ERROR - create_log_symlink_err:".format(now_time),create_log_symlink_err)
        return stream
