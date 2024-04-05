---
date: 2024-04-05T14:37:41.125300
author: AutoGPT <info@agpt.co>
---

# Availability Checker

To develop a function that returns the real-time availability of professionals, updating based on current activity or schedule, a system has been conceptualized using a tech stack involving Python, FastAPI, Prisma, and PostgreSQL. The requirements gathered indicate that the system should cater to professions such as healthcare professionals, emergency services personnel, IT support specialists, and customer service representatives, which necessitates a high degree of reliability and real-time responsiveness. 

The proposed solution will utilize FastAPI to create RESTful API endpoints for managing user profiles, schedules, and availability updates. PostgreSQL, with Prisma as the ORM, will serve as the backend database, capable of storing and managing time-sensitive data, following best practices such as utilizing appropriate data types for time representation and implementing partitioning on time-based columns for optimized performance. 

For real-time updates, the system will leverage WebSocket for bi-directional communication between the client and server. This will enable instant notification of availability changes triggered by various conditions such as acceptance of new projects, completion of tasks, or unexpected events like emergencies. On the server side, logical replication or triggers in PostgreSQL will be used to listen to change events and update the professional's availability status, which will then be broadcasted to relevant parties through WebSocket connections. 

This approach ensures that the system can reliably track and update the availability status of professionals in real-time, enhancing the efficiency of emergency response, patient care, technical support, and customer service. It also provides a framework for scalability, allowing for the addition of more professions or customization of triggers for availability updates as needed.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Availability Checker'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
