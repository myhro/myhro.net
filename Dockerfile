FROM debian:wheezy
RUN apt-get update
RUN apt-get install -y adduser build-essential libgeoip1 libpq-dev python-dev python-pip
RUN addgroup --gid 2000 gunicorn
RUN adduser --disabled-password --ingroup gunicorn --no-create-home --system --uid 2000 gunicorn
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
