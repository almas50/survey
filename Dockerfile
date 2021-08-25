FROM python:alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -U pip
RUN pip install gunicorn psycopg2
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY . /src/
RUN python manage.py migrate
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "8", "survey.wsgi"]