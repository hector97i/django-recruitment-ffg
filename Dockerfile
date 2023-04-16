FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CONFIG 'config.json'

RUN apt update
RUN apt install gcc -y
RUN pip install 'poetry==1.3.1'

COPY pyproject.toml poetry.lock .
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./setup.cfg .
COPY ./api ./api
COPY ./images ./images
COPY ./image_app ./image_app
COPY ./manage.py ./manage.py
COPY ./config.json .

COPY ./config ./config
COPY ./entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 80

CMD ./entrypoint.sh
