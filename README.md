## Weather Web App

A simple weather web app using python, flask and mysql; constructed with the help of this following tutorial: [click me](https://www.youtube.com/watch?v=lWA0GgUN8kg).

## Installation and Setup Instructions

Clone this repository. Run `pip install -r requirements.txt`.

## Environment Variables
Create a `.env` file with the following structure:<br><br>
HOST = "YOUR_MYSQL_HOSTNAME"<br>
USER = "YOUR_MYSQL_USER_NAME"<br>
PASSWD = "YOUR_MYSQL_PASSWORD"<br>
DATABASE = "YOUR_MYSQL_DATABASE_NAME"<br><br>
Filling in the required information with your mysql details.

## Database Setup
Run the `create_dbs.py` script to create the database in mysql.

## Running Web App:
Run `python app.py` and the web app will be run in your localhost.

## Viewing Logs
Logs can be viewed at `log/record.log`