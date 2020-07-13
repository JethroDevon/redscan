

from datetime import datetime

class LoggingObject:
    
    def __init__(self, logType, output):

        print ("-" + logType + "-#" + str(datetime.now()) + "#" + output + "\n")
