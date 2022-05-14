FROM python:3.8.13-slim
COPY ./utils ./utils
COPY ./data_generator ./
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt
CMD python data_generator.py