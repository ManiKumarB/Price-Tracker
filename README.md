# Price-Tracker
 The application will help people to receive alerts through email when the price of a product drops in amazon.in 

This is a web application designed with python, selenium and streamlit framework.

## Dependencies
Install the dependencies using following command:
```bash
pip install -r requirements.txt
```
Download [chromedriver](https://chromedriver.chromium.org/downloads)

## First step
Create the table to store the registered users
```bash
python Table Creation.py
```
It creates RegisteredUsers.db file for storing subscribed users to send alerts when price drops

## Second step
To run the program
```bash
streamlit run run.py
```
I am using SMTP gmail server for sending product details to user.
To access application : http://localhost:8501/

## Third step
To schedule the program
```bash
python Schedule.py
```
Retrieve the db file and checks if any price drops
