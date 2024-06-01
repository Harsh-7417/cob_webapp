git clone <your-github-repo-url>

cd cob_webapp

docker-compose up --build

docker-compose run backend-tests

docker volume rm cob_webapp_db_data
