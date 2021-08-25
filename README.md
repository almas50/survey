# Survey

### Run app

```
cp .env.example .env 
docker-compose up
```

### Documentation

```
swagger localhost:8000/swagger
```

### Development

```
virtualenv venv
source venv/bin/activate 
pip install -r requirements.txt
cp .env.example .env 
python manage.py migrate
python manage.py runserver
```