# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* |   Single Server - Basic - 1 vCore - 21 GB  |    $34.58        |
| *Azure Service Bus*       |   Basic - 1 Million                        |    $0.5          |
| *Azure Function App*      |   1 Million call - 5000 ms time            |    $3.60         |
| *Azure Web App*           |   Free                                     |    Free          |
| Total                     |                                            |    $38.23        |

## Architecture Explanation
1. Scenario
- If we are triggering mail through the web app, if there are 1000 attendees the user must wait on the notification page until all attendees are notified due to this timeout issues can easily occur. 
- In order to efficiently handle the sending of emails in the background, it is necessary to separate it from the main web application. The web app should only handle listing and queuing tasks, which can be done using the Free Tier since the web traffic is not very high.
- The cost of sending emails will depend on factors such as the number of attendees and how many emails are sent, which may increase the monthly cost due to longer execution times. However, using Azure Function App is a cost-effective solution that allows the web app to have more resources without incurring high expenses.
2. Drawbacks: 
The previous implementation of the application had the following pain points:
- The web application is not scalable to handle user load at peak
- When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
- The current architecture is not cost-effective
3. Advantages
- Migrating the existing web app to an Azure App Service takes cares of scaling constraint, improves operation cost efficiency
- Migrating PostgresSQL to scalable Azure database services allow developers to focus on database structures and operations instead of applying security or update patches. The $36.36 monthly cost on the Basic tier is more than offset by the cost savings gained.
- Through the migration to a microservice architecture and refactoring the notification logic to an Azure Function via a service bus queue message, the different components of the web application are decoupled. This makes it more scalable and sending out of notifications does not lead to HTTP timeout exceptions anymore.
