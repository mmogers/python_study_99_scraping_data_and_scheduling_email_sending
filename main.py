import schedule
import time
import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = os.environ['mailPass']
username = os.environ['mailUsername']

def getNews():
    url = "https://replit.com/community-hub"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    link_tags = soup.find_all('a', {"class": "css-epm014"})

    news_list = []
    for link_tag in link_tags[:3]:  # Take the first three links and titles
        link = link_tag['href']
        title_tag = link_tag.find('span', {'class': 'css-scxoy8'})
        title = title_tag.text if title_tag else "Title not found"
        news_list.append(f"{title}. \n{link}. \n")

    return news_list

def sendEmail(news_list):
    if not news_list:
        return  # No news found

    server = "smtp.gmail.com"
    port = 587
    s = smtplib.SMTP(host=server, port=port)
    s.starttls()
    s.login(username, password)

    msg = MIMEMultipart()
    msg['To'] = "marinamoger@yahoo.com"
    msg['From'] = username
    msg['Subject'] = "Top 3 community events!"

    for news_item in news_list:
        msg.attach(MIMEText(news_item, 'plain'))

    s.send_message(msg)
    del msg

def printMe():
    print("⏰ Sending reminder")
    news_list = getNews()
    sendEmail(news_list)

schedule.every(15).seconds.do(printMe)

while True:
    schedule.run_pending()
    time.sleep(1)
