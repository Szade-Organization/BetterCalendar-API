#Dockerfile

FROM python:3.11

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8000

ENTRYPOINT [ "python", "config/manage.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "core.wsgi:application"]