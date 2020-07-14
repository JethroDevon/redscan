#!/usr/bin/env python3
import sqlite3, urllib.request, sys
from datetime import datetime
from loggingObject import LoggingObject

#on initialisation args have to point to a hosted CSV, database may as well handle auth request
class DB:

    csv_data = ""
     
    #initialise new database and write data to it found at the url passed into its arguments
    #on initialising this data will be parsed into the database row by row
    def __init__(self, csv_url):

            self.table_name = "sample_data" #database at init is default called "sample_data"

            #create url request for embedded csv file
            req = urllib.request.Request(csv_url)
            urllib.request.urlopen(req)

            #read file data onto csv_data object
            with urllib.request.urlopen(req) as response:
                csv_data = response.read()
                csv_data = str(csv_data,"utf-8")

            #split table into rows
            csv_data = str(csv_data).split('\n')
            self.createDatabase(self.table_name, csv_data)
                
    #this takes a string array for sample data table and validates each row, maybe if does not validate returns false else true and commits
    #TO DO: limit size of new entries to avoid truncation. TD add time stamp
    def createDatabase(self, tablename, csv_data_arr):
        
        try:
                                
            #create table in memory and connect to it, move cursor to start position and write CSV row data to table line by line
            self.db_conn = sqlite3.connect(':memory:')
            cur = self.db_conn.cursor()
            cur.execute("CREATE TABLE " + tablename + "(" + csv_data_arr[0] + ",submissionT,Uread);")         
             
            #loops through each row of data and loads onto table after some sanitisation
            for rows in range(1, len(csv_data_arr)-1):
            
                row = self.sanitizeRow(csv_data_arr[rows])                       
                sql = "INSERT INTO " + tablename + " (" + csv_data_arr[0] + ",submissionT,Uread) VALUES (" + row + ");"              
                cur.execute(sql)
                
            self.db_conn.commit()        
            LoggingObject("INIT","database created with " + str(self.countRows(cur, tablename)) + " rows")
            
        except sqlite3.Error as e:
            LoggingObject("ERROR", "initialisation failed: " + str(e))
        
        except Exception as e:
             return LoggingObject("ERROR", str(e))
           

    #time is in format %y%m%d%H%m, year 20 month 07 day hour 14 minute 13 therefore would look like 20071413
    def timeRequest(self, start, end):        

        try:
            cur = self.db_conn.cursor()
            cur.execute("SELECT * FROM " + self.table_name + " WHERE submissionT BETWEEN " + start + " AND " + end)
            return cur.fetchall()

        except sqlite3.Error as e:
            return LoggingObject("ERROR", "time request failed: " + str(e))

        except Exception as e:
             return LoggingObject("ERROR", str(e))
           
    #can search a column for a value, it will return a row
    def standardRequest(self, column, value):
   
        try:
            cur = self.db_conn.cursor()
            cur.execute("SELECT * FROM " + self.table_name + " WHERE " + column + "=\"" + value + "\"")
            return cur.fetchall()

        except sqlite3.Error as e:
            return LoggingObject("ERROR", "standard request failed: " + str(e))
        
        except Exception as e:
             return LoggingObject("ERROR", str(e))

    def setURead(self, id, status):
   
        try:
            cur = self.db_conn.cursor()
            cur.execute("UPDATE " + self.table_name + " SET Uread=\"" + status + "\" WHERE policyID=" + id + "")
            return "updated"

        except sqlite3.Error as e:
            return LoggingObject("ERROR", "set uread column failed: " + str(e))
        
        except Exception as e:
             return LoggingObject("ERROR", str(e))

    def tableInfo(self):
   
        try:
            cur = self.db_conn.cursor()
            cur.execute("SELECT * FROM pragma_table_info(\'" + self.table_name + "\')")
            return str(cur.fetchall())
            
        except sqlite3.Error as e:
            return LoggingObject("ERROR", "table Info failed: " + str(e))
        
        except Exception as e:
             return LoggingObject("ERROR", str(e))
           
    #def tokenRequest(self, username, password_hash):

        #try:
            #find user
            #cur = new stuff get new stuff
            #pull it up with salt cake salt
            #add the data to the pulled up caked hash
            #compare them
            #reply nope or overwrite the existing token in the database and return it
            
            #except sqlite3.Error as e:
            #return LoggingObject("ERROR", "time request failed: " + str(e))
            
        #except Exception as e:
            # return LoggingObject("ERROR", str(e))
           
    
    def countRows(self, cursor, table):

        cursor.execute("select * from " + table)
        return len(cursor.fetchall())

    #sanitizes a row, splits up rows into each individual entry and wraps strings in quotes, adds time stamp read columns 
    #TD: tweak to use later with json checker
    def sanitizeRow(self, row):

        dtime = self.time()
        PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/_-=&,"     
        row = "".join(c for c in row if c in PERMITTED_CHARS)
        entries = row.split(",")
        row = ""
        
        for entry in entries:

            if(not(self.isfloat(entry) or self.isint(entry)) and isinstance(entry, str)):
                entry = "\"" + entry + "\""
            row += entry + ","
            
        row += dtime + ",\"unread\""
        
        return row
                        
    def isfloat(self,x):
        try:
            a = float(x)
        except ValueError:
            return False
        else:
            return True

    def isint(self,x):
        try:
            a = float(x)
            b = int(a)
        except ValueError:
            return False
        else:
            return a == b

    #time stamp with set format for various funcions
    def time(self):
        
        dtime = datetime.now()
        dtime = dtime.strftime("%y%m%d%H%M")
        return str(dtime)
