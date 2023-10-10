import azure.functions as func
import logging
import psycopg2
from datetime import datetime
from sendgrid.helpers.mail import Mail

app = func.FunctionApp()
@app.service_bus_queue_trigger(arg_name="azservicebus", queue_name="notificationqueue",
                               connection="notificationqueue") 
def sendnotification(azservicebus: func.ServiceBusMessage):
    notification_id = int(azservicebus.get_body().decode('utf-8'))
    logging.info('Python ServiceBus Queue trigger processed a message: %s', notification_id)

    # get connection to database
    db_connection = psycopg2.connect(db_name="techconfdb", user="mig_account@migration-project-server01", password="Pass@word1", host="migration-project-server01.postgres.database.azure.com")
    cursor = db_connection.cursor()
    
    try:
        # get notification message and subject from database using the notification_id
        notification_query =  cursor.execute("SELECT message, subject FROM notification WHERE id = %s;", (notification_id,))
        
        # get attendees email and name
        cursor.execute("SELECT first_name, last_name, email FROM attendee;")
        attendees = cursor.fetchall()
        
        # loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
            Mail('{}, {}, {}'.format({'admin@techconf.com'}, {attendee[2]}, {notification_query}))
    
        notification_completed_date =  datetime.utcnow()
        notification_status = 'Notified {} attendees'.format(len(attendees))

        # update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cursor.execute("UPDATE notification SET completed_date = %s, status = %s WHERE id = %s;", (notification_completed_date, notification_status, notification_id,))
        db_connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        db_connection.rollback()
    finally:
        # close connection
        cursor.close()
        db_connection.close()
