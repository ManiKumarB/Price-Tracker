import streamlit as st
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import sqlite3
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@st.cache(suppress_st_warning=True)
def getDetails(keyword):
    df = pd.DataFrame()
    Links = []
    Titles = []
    Price = []
    driver = webdriver.Chrome('#CHROMEDRIVER PATH eg:chromedriver.exe')
    driver.get("https://www.amazon.in/")
    driver.find_element_by_id("twotabsearchtextbox").send_keys(keyword)
    driver.find_element_by_class_name("nav-input").click()
    time.sleep(6)
    list_url = driver.find_element_by_class_name("s-result-list")
    results = list_url.find_elements_by_xpath("//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
    links = [link.get_attribute('href') for link in results]
    for i in links[0:3]:
        short_url = i.split("/dp/")[0]+"/dp/" + i.split("/dp/")[1].split("/ref")[0]
        Links.append(short_url)
        driver.get(f'{short_url}?language=en_GB')
        Titles.append(driver.find_element_by_id('productTitle').text)
        try:
            Price.append(driver.find_element_by_id('priceblock_ourprice').text)
        except NoSuchElementException:
            try:
                Price.append(driver.find_element_by_id('priceblock_dealprice').text)
            except Exception as e:
                Price.append("Can't get price of a product")
        except Exception as e:
            Price.append("Can't get price of a product")
    driver.close()
    df["Link"] = Links
    df["Title"] = Titles
    df["Price"] = Price
    return df

@st.cache(suppress_st_warning=True)
def singleProductDetails(short_url):
    df = pd.DataFrame()
    # short_url = url.split("/dp/")[0]+"/dp/" + url.split("/dp/")[1].split("/ref")[0] + "?language=en_GB"
    driver = webdriver.Chrome('#CHROMEDRIVER PATH eg:chromedriver.exe')
    driver.get(short_url)
    title = driver.find_element_by_id('productTitle').text
    try:
        price = driver.find_element_by_id('priceblock_ourprice').text
    except NoSuchElementException:
        try:
            price = driver.find_element_by_id('priceblock_dealprice').text
        except Exception as e:
            price = "Can't get price of a product"
    except Exception as e:
        price = "Can't get price of a product"
    driver.close()
    df["Link"] = [short_url]
    df["Title"] = [title]
    df["Price"] = [price]
    return df

def emailRegister(email, df):
    pd.set_option('colheader_justify', 'center')
    sender_email = "mail@gmail.com"
    receiver_email = email
    password = "password"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Price Tracker For U"
    message["From"] = sender_email
    message["To"] = receiver_email
    html = """\
        <html>
          <head>
          </head>
          <body>
            {0}
            <br/><br/>
            Thanks for subscribing with us, We will send alerts when price drops.
            <br/><br/><br/>
            Regards,<br/>
            Price Tracker For U.
          </body>
        </html>
        """.format(df[['Link', 'Title', 'Price']].to_html(index=False))
    part2 = MIMEText(html, "html")
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def registerDB(final_df, email):
    conn = sqlite3.connect('RegisteredUsers.db')
    for index, row in final_df.T.iteritems():
        Price = str(row.Price.split("₹ ")[1])
        if "," in Price:
            Price = Price.split(",")[0]+Price.split(",")[1]
        conn.execute("INSERT INTO COMPANY VALUES(" + "'" + row.Link + "','" + row.Title + "'," + Price + ",'" + email + "')")
    conn.commit()
    conn.close()


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black;'>Price Tracker For U</h1>", unsafe_allow_html=True)

# st.title('Price Tracker for U')
selection = st.selectbox("How would you like the select products?", ("Keyword", "URL"))

if selection == "Keyword":
    keyword = st.text_input("Enter the product name you like to track")
    if len(keyword) > 0:
        final_df = pd.DataFrame()
        df = getDetails(keyword)
        st.dataframe(df[["Title", "Price"]])
        selected_indices = st.multiselect('Select rows:', df.index)
        selected_rows = df.loc[selected_indices]
        st.write('Selected Rows', selected_rows[["Title", "Price"]])
        final_df = final_df.append(selected_rows, ignore_index=True)
        if len(final_df) > 0:
            email = st.text_input("Enter your mail to subscribe for price drop alerts")
            if len(email) > 10:
                registerDB(final_df, email)
                emailRegister(email, final_df)

if selection == "URL":
    url = st.text_input("Enter the amazon.in URL you like to track")
    if len(url) > 0:
        if "https://www.amazon.in/" in url:
            df = singleProductDetails(url)
            st.dataframe(df[["Title", "Price"]])
        else:
            st.error("Check the URL")
        if len(df) > 0:
            email = st.text_input("Enter your mail to subscribe for price drop alerts")
            if len(email) > 10:
                registerDB(df, email)
                emailRegister(email, df)
