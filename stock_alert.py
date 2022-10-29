'''Sends email alerts once stock price limit is triggered.'''

import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt
import time

import smtplib
import os
from email.message import EmailMessage


sender_id = os.environ.get('email_id')
sender_pass = os.environ.get('email_password')
receiver = 'megh1128uk@gmail.com'

msg = EmailMessage()

yf.pdr_override()
start = dt.datetime(2022, 10, 11)
end = dt.datetime.now()
ticker = 'LLOY.L'
low_target = 40
high_target = 41

alert = False


def send_alert(subject, body):
    '''Sends email alert.'''

    msg['From'] = sender_id
    msg['To'] = receiver
    msg[subject] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_id, sender_pass)
        smtp.send_message(msg)


def main():
    while alert != True:

        data = pdr.get_data_yahoo(ticker, start, end)

        price = data['Adj Close'][-1]
        print(price)

        if price < low_target and alert == False:
            subject = 'Alert! Stock price going down!'
            body = f"The stock price of {ticker} is now {price} GBP.\nTarget low price was {low_target} GBP. Maybe it's time to buy?"
            send_alert(subject, body)
            alert = True
            print("\nCompleted!")
        elif price > high_target and alert == False:
            subject = 'Alert! Stock price going up!'
            body = f"The stock price of {ticker} is now {price} GBP.\nTarget high price was {high_target} GBP. Maybe it's time to sell?"
            send_alert(subject, body)
            alert = True
            print("\nCompleted!")
        else:
            print("\nNo new alerts!")
            time.sleep(60)


if __name__ == '__main__':
    main()
