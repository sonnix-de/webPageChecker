
import requests        # Import requests (to download the page)
# Import BeautifulSoup (to parse what we download)
# from bs4 import BeautifulSoup
import time             # Import Time (to add a delay between the times the scape runs)
import smtplib          # Import smtplib (to allow us to email)
import configparser
import os
import logging


def getEmailRecipients(reciepients):
    ergebnis = reciepients.split(";")
    return ergebnis


def sendMail(subject,content):
    config = configparser.ConfigParser()
    config.read('.env')    
    SMTP_SERVER = config.get('EMAIL','smtp_server')
    SMTP_PORT = config.get('EMAIL','smtp_port')
    SMTP_USERNAME = config.get('EMAIL','adresse')
    SMTP_PASSWORD = config.get('EMAIL','password')
    EMAIL_FROM = config.get('EMAIL','adresse')
    EMAIL_TO = config.get('APP','recipients')
    EMAIL_SUBJECT = subject

    
    
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(SMTP_USERNAME, SMTP_PASSWORD)
    message = 'Subject: {}\n\n{}'.format(subject, content)
    recpients = getEmailRecipients(EMAIL_TO)
    s.sendmail(EMAIL_FROM, recpients, message)
    s.quit()    
    return



if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('.env')
    logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG)    
    
    url = config.get('APP','URL')
    secondsToWait = int(config.get('APP','secondsToWait'))
    contentCacheFile= config.get('APP','CONTENT_CACHE_FILE')
    cacheContent = ""
    # while this is true (it is true by default),
    while True:
        if os.path.exists(contentCacheFile):
        
            f = open(contentCacheFile,"r")
            cacheContent = f.read()
            #print ("oldContent=",cacheContent)
        
        # set the headers like we are a browser,
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        # download the homepage
        response = requests.get(url, headers=headers)
        newContent = response.text
        # und schreibe sie in das file:
        f = open(contentCacheFile, "w")
        f.write(newContent)
        f.close()
        # hat sich was geändert?
        if (cacheContent == newContent):
            logging.info('keine Aenderung')
            # wait x seconds,
            time.sleep(secondsToWait)
            continue # continue with the script,
            
        # bei änderungen werde aktiv
        else:

            print ("\a") # beep
            message = "der Inhalt der Webseite hat sich geaendert. siehe: {}".format(url)
            sendMail("Aenderung bei Webseite",message)
            continue # continue with the script,
