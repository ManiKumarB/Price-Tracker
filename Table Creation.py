import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('RegisteredUsers.db')

conn.execute('''CREATE TABLE COMPANY(Link VARCHAR(1000),
                                     Title VARCHAR(1000),
                                     Price INT,
                                     Email VARCHAR(25));''')
conn.commit()
conn.close()

