FROM python:3.11.1-slim-bullseye AS python_image

RUN pip install --upgrade pip
RUN apt update && apt install build-essential curl -y
RUN pip install poetry

WORKDIR /app

COPY ["poetry.lock","pyproject.toml","./"]

RUN poetry install --without dev

COPY ./src src

#I have temporarily copied the tests. We can ignore once we integrate it with CICD. It will help in reducing size of production image
COPY ./tests tests  

EXPOSE 8000

CMD ["poetry","run","uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
