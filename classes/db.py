#!/usr/bin/env python3
import sqlite3, urllib.request, sys
from loggingObject import LoggingObject

#on initialisation args have to point to a hosted CSV, database may as well handle auth request
class DB:

    #read could be toggled for specific users having read by database rather than
    read = False
    csv_data = ""
    
    #initialise new database and write data to it found at the url passed into its arguments
    #on initialising this data will be parsed into the database row by row
    def __init__(self, csv_url):

        try:

            #create url request for embedded csv file
            req = urllib.request.Request(csv_url)
            urllib.request.urlopen(req)

            #read file data onto csv_data object
            with urllib.request.urlopen(req) as response:
                csv_data = response.read()
                csv_data = str(csv_data,"utf-8")

            #split table into rows
            csv_data = str(csv_data).split('\n')

            #create table in memory and connect to it, move cursor to start position and write CSV row data to table line by line
            db_con = sqlite3.connect(':memory:')
            c = db_con.cursor()
            db_con.execute("CREATE TABLE sample_data(" + csv_data[0] + ");")
            #db_con.execute("INSERT INTO sample_data VALUES (1, 'bruce'), (2, 'wayne'), (3, 'BATMAN');")
            db_con.commit()
            
        except sqlite3.Error as e:

            LoggingObject("ERROR",str(e))
            
       
        
    #def timeRequest(start, end):

    #def paramRequest(param):

    def toggleRead():

        if(read):
            read = False
        else:
            read = True
