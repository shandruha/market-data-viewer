FROM python:3.8.13-slim
COPY ./utils ./utils
COPY ./app ./
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt
CMD gunicorn -b 0.0.0.0:80 app:server