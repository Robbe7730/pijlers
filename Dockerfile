FROM python:3.9
MAINTAINER Robbe Van Herck <robbe@robbevanherck.be>

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY static/ /app/static
COPY templates/ /app/templates
COPY *.py /app/

ENTRYPOINT python app.py
