FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1
RUN mkdir /app
WORKDIR /app
EXPOSE 8000

RUN apt-get update && apt-get install -y pkg-config

COPY requirements.txt .
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/mysql -lmysqlclient"
RUN pip install -U pip && pip install -r requirements.txt

COPY manage.py .
COPY . /app

CMD python manage.py collectstatic --no-input
CMD gunicorn backend.wsgi:application -b 0.0.0.0:8000