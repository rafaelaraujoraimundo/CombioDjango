FROM python:3.11-slim

RUN apt update
RUN apt-get install libmariadb-dev-compat -y
RUN apt install pkg-config -y
RUN apt-get install gcc -y
COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic
#RUN python manage.py migrate
CMD ["gunicorn", "combio.wsgi:application", "-b", "0.0.0.0:8000", "--workers", "4"]