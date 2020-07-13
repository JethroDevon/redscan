from datetime import datetime

class LoggingObject(logType, output):

    def __init__(self, logType, output):
        print ("-" + logType + "-#" + datetime.now() + "#" + output + "\n")
