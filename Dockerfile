from python:3.7.8-buster

RUN pip3 install requests flask-restfull pytest-flask 

ENV FLASK_APP=ghibli
ENV FLASK_ENV=dev

RUN flask run -p 8000
