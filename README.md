# Price-Tracker
 The application will help people to receive alerts through email when the price of a product drops in amazon.in 

This is a web application designed with python, selenium and streamlit framework.

## Dependencies
Install the dependencies using following command:
```bash
pip install -r requirements.txt
```


## First step
Create the table to store the registered users
```bash
python Table Creation.py
```
Stores the subscribed users for sending alerts when price drops

## Second step
To run the program
```bash
streamlit run run.py
```
To access application : http://localhost:8501/

## Third step
To schedule the program
```bash
python Schedule.py
```
Retrieve the db file and checks if any price drops
