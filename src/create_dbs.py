import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import pytz
from dotenv import load_dotenv

load_dotenv() # load environment variables form .env

#######################################################################################################
#######################################################################################################

# create database
myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'))

cur = myconn.cursor()

try:
    cur.execute("CREATE DATABASE weather")
except:
    myconn.rollback()

myconn.close()

#######################################################################################################
#######################################################################################################

myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

cur = myconn.cursor()

try:
    # create the table and insert one value
    dbs = cur.execute('CREATE TABLE city(id INT AUTO_INCREMENT NOT NULL,city_name VARCHAR(100),PRIMARY KEY(id));')
    print("==============> TABLE CREATED SUCCESSFULLY <==============")
    dbs = cur.execute('INSERT INTO weather.city (city_name) values ("Johannesburg");')
    myconn.commit()
    print("==============> VALUE INSERTED SUCCESSFULLY <==============")
    
except:
    myconn.rollback()

myconn.close()