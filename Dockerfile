#Dockerfile

FROM python:3.11

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8000

CMD  python config/manage.py migrate;python config/manage.py populate -u 3 -c 20 -a 300;python config/manage.py runserver 0.0.0.0:8000