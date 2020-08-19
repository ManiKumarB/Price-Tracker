from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import sqlite3
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def singleProductDetails(short_url):
    df = pd.DataFrame()
    # short_url = url.split("/dp/")[0]+"/dp/" + url.split("/dp/")[1].split("/ref")[0] + "?language=en_GB"
    driver = webdriver.Chrome("#CHROMEDRIVER PATH eg:chromedriver.exe")
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
    return price

def emailSend(email, df):
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
            Thanks for subscribing with us, We found that your subscribed product drops.
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

def scheduleProgram():
    conn = sqlite3.connect('RegisteredUsers.db')
    data = pd.read_sql("SELECT * FROM COMPANY", conn)
    for index, row in data.T.iteritems():
        print("------------")
        print(row)
        print("------------")
        pre_price = row["Price"]
        post_price = singleProductDetails(row["Link"])
        try:
            post_price = str(post_price.split("₹ ")[1])
            if "," in post_price:
                post_price = post_price.split(",")[0]+post_price.split(",")[1]
            if post_price < pre_price:
                data.loc[index, "Price"] = post_price
                emailSend(row["Email"], row)
        except:
            pass

schedule.every().hour.do(scheduleProgram)
while True:
    schedule.run_pending()
    time.sleep(1)
