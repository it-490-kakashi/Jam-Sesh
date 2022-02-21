FROM python:3.8-alpine

COPY ./requirements.txt /
RUN pip install -r /requirements.txt

ADD . /flask_app
WORKDIR /flask_app

CMD flask run --host=0.0.0.0