
from datetime import datetime

class LoggingObject:

    def __new__(cls, logType, output):

        cls.log = "-" + logType + "-#" + str(datetime.now()) + "#" + output
        print (cls.log)
        return cls.log
