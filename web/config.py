import os
import logging

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL= os.getenv('POSTGRES_URL') or "migration-project-server01.postgres.database.azure.com"
    logging.info("POSTGRES_URL: " + POSTGRES_URL)
    print("POSTGRES_URL: " + POSTGRES_URL)
    POSTGRES_USER= os.getenv('POSTGRES_USER') or "mig_account@migration-project-server01"
    POSTGRES_PW= os.getenv('POSTGRES_PW') or "Pass@word1"
    POSTGRES_DB= os.getenv('POSTGRES_DB') or "techconfdb"
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://notificationservicebus1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=KcJJV5m4rvGbBP+cWILeleXUdMXIdiFkR+ASbJAhMtk='
    SERVICE_BUS_QUEUE_NAME = os.getenv('SERVICE_BUS_QUEUE_NAME') or 'notificationqueue'
    ADMIN_EMAIL_ADDRESS = os.getenv('ADMIN_EMAIL_ADDRESS') or 'chaunn3502@gmail.com'
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY') or '' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False