FROM python:3.6-alpine

RUN pip install -r requirements.txt

EXPOSE 8080
CMD python -O runserver.py config.ini
