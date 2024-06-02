# Cost of borrowing (COB)

## Overview
This project collects data from the European Central Bank's (ECB) APIs for the series "Cost of borrowing for households for house purchase - euro area, Euro area (changing composition), Monthly". The collected data is stored in PostgreSQL through an api endpoint provided by the backend(FastApi). Finally, a React web page using Chart.js displays the data from the backend as a line graph.


## Components

The project consists of the following components:

- __Database__: Postgres to store the data fetched from ECB endpoint.
- __FastAPI Backend__: Have endpoints to interact with postgres DB and frontend.
- __React Frontend__: Web page built with React and Chart.js to visualize the data fetched from backend API(s)
- __Dockerization__: Docker containers for each component.
- __docker-compose.yml__: Docker Compose file to run all components together. It contains all the required dependencies including health checks to run the application in right order.


## Prerequisites
Before running this project, make sure you have the following installed:
- [Docker][https://docs.docker.com/compose/install/]
## Usage
To run the project, follow these steps:

1. Clone the git repository:
    ```bash
    git clone git@github.com:Harsh-7417/cob_webapp.git
    ```
2. Navigate to the project directory:
    ```bash
    cd cob_webapp
    ```

3. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```

4. If you want to run backend tests:
    ```bash
    docker-compose run backend-tests
    ```

## Test application
http://localhost:3000/

For the very first time, the line graph will be empty as at this time we don't have any data in database table. To load the data, we have two options:

1) On web page, there is refresh button at top right corner. If you click, it will call the backend endpoint which will fetch the data from ECB endpoint and will load into database table.
2) Directly through the backend endpoint. To access all backend endpoints, you can visit http://localhost:8000/docs

## Clean Up
To clean up Docker volumes after running the project, you can use the following command:
```bash
docker-compose down --volumes
```

## Key architectural decisions/considerations: {#key-decisions}
**Question 1** : Should we load the data on every api hit?

**Answer** : Analyzed the data, and learnt that data updation is not frequent and mostly happen once in a month. Hence it doesn't make sense to refresh the data in database on every call. I have designed the backend system to use http response code 304 from the ECB api, which means data will be only loaded/refreshed in our database if there is any change in data from ECB.

**Question2** : Should we only load updates in our database, or should we do truncate and load on data change?

**Answer**: Given it is monthly aggregated data and have only one record per month. So, even if it is 100 years of data, it will be only 100*12 = 1200 records. Hence, it doesn't make much sense to compare and insert the updates. Rather, truncate and load will be really fast operation for such activity. However, there is a small risk associated, if the data gets truncated but failed to insert for some reason. We can mitigate this risk by having a backup table. 

After trade off,I have decided to go with truncate and load, with proper rollback mechanism in case of failures.

## Some corner cases

**Scenario** : What will happen if data accidently gets deleted from table?

Backend will reset the required pointer and will load the latest data again.

**Scenario** : What if we get error processing the data, will backend still truncate the table?

Backend is designed with proper exception handling and will prevent the table to truncate.

**Scenario** : What if the table gets deleted accidently? How fast we can recover?

Just redploy the Backend system and it will create all required tables.

**Scenario** : Will backend create the table on every deployment?

No, It will only create if table does not exist.


## To-Do
- [ ] Write unit tests for frontend.
- [ ] Increase unit test coverage for backend.
- [ ] Move environment variables from .env to more secured approaches.
- [ ] Decide on database maintenance like backing up, versioning of tables. We can use something like alembic.
- [ ] Decide if we want to keep frontend and backend in their own repo's
- [ ] Make it production ready - Integrate with CICD , integration tests, infrastructure as a code, log monitoring etc. It all depends on product vision and roadmap.