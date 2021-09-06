FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt update && apt install python3-dev -y

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

WORKDIR /code

COPY Pipfile* /code/

RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip3 install -r requirements.txt

COPY backend /code/backend/
COPY frontend /code/frontend/
COPY uploads /code/uploads/
COPY public /code/public/

WORKDIR /code/backend

