import requests
import string
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask import Flask, request, render_template, redirect
import mysql.connector
from dotenv import load_dotenv
import logging

# setup logger
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='log/record.log', filemode='w',format=FORMAT)
logger.setLevel(logging.WARNING)

# importing environment variables
load_dotenv()

# initialising flask app
app = Flask(__name__)
# setting app secret key
app.secret_key = "hiruzen_sakatoshi"

# Function to pull weather data form api
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=b21a2633ddaac750a77524f91fe104e7"
    r = requests.get(url).json()
    return r

def get_cities():
    '''This function returns all the cities in the databse'''
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    
    try:
        query = "SELECT city_name FROM weather.city"
        cur.execute(query)

        myresult = cur.fetchall()

    except mysql.connector.DatabaseError:
        myconn.rollback()

    myconn.close()
    # neatening the returned list
    gc = [var[0] for var in myresult]
    return gc

def city_exists(city):
    '''This is a boolean function to check if a city already exists in the db'''
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    
    try:
        query = "SELECT EXISTS(SELECT * FROM weather.city WHERE city_name = '" + city + "');"
        cur.execute(query)

        myresult = cur.fetchall()

    except mysql.connector.DatabaseError:
        myconn.rollback()

    myconn.close()

    return myresult[0][0]

# Function to insert into db
def insert_city(city):
    '''This function inserts a city into the database'''
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    
    try:
        query = "INSERT INTO weather.city (city_name) VALUES ('" + city + "')"
        cur.execute(query)
        myconn.commit()

    except mysql.connector.DatabaseError:
        myconn.rollback()

    myconn.close()

def del_city(city):
    '''This function deletes a city form the database'''
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    
    try:
        query = "DELETE from weather.city WHERE city_name = '" + city + "'"
        cur.execute(query)
        myconn.commit()

    except mysql.connector.DatabaseError:
        myconn.rollback()

    myconn.close()

# Index Page
@app.route('/', methods=['GET','POST'])
def index():
    # if POST request
    if request.method == 'POST':
        try:
            err_msg = ''
            # get city from from
            new_city = request.form.get('city')
            new_city = new_city.lower()
            new_city = string.capwords(new_city)
            # check if the city already exists
            if new_city:
                existing_city = city_exists(new_city)
                # if it doesn't already exist...
                if not existing_city:
                    new_city_data = get_weather_data(new_city)
                    # checking if the city is valid
                    if new_city_data['cod'] == 200:
                        # insert into db if it passes both checks
                        insert_city(new_city)
                    # if not valid return relvant error message
                    else:
                        err_msg = 'That is not a valid city!'
                # if it already exists return relevant error message
                else:
                    err_msg = 'City already exists in the database!'
            # log and flash the error message if there is one
            if err_msg:
                logger.warning(err_msg)
                flash(err_msg, 'error')
            # otherwise log and flash a success message
            else:
                logger.warning('City added successfully!')
                flash('City added successfully!', 'success')
            # redirect to the same index page; effectively a refresh
            return redirect(url_for('index'))
        except:
            logger.critical('A critical error has occured')
    # if GET request
    else:
        try:
            # fetch all cities from the db
            cities = get_cities()

            weather_data = []

            # for every city fetched - get its weather data from the api, create a dictionary of the relevant data and store it in a list of all cities  relevant weather data
            for city in cities:
                r = get_weather_data(city)
                weather = {
                    'city' : city,
                    'temperature' : r['main']['temp'],
                    'description' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon'],
                }
                weather_data.append(weather)

            # log a succesful retreival of the weather data
            logger.warning('Succesfully loaded weather data!')
            # render the weather template, passing the data needed to display the weather for each city
            return render_template('weather.html', weather_data=weather_data)
        except:
            logger.critical('A critical error has occured')

# Deleting a City Route
@app.route('/delete/<name>')
def delete_city( name ):
    # deletes a city form the db
    del_city(name)
    # logs and flashes a succesful deletion
    logger.warning(f'Successfully deleted { name }!')
    flash(f'Successfully deleted { name }!', 'success')
    # effectively refreshes
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)