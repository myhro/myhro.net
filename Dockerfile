FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy build-essential libgeoip1 libpq-dev python-dev python-pip

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--log-file", "-", "myhronet.wsgi"]
