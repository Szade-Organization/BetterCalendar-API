#Dockerfile

FROM python:3.11

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8000

CMD  source setup-populate.sh; python config/manage.py runserver 0.0.0.0:8000