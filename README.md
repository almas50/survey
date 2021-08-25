
### Run 

```
cp .env.example .env 
docker-compose up

OR

pip install -r requirements.txt
cp .env.example .env 
python manage.py migrate
python manage.py runserver
```

### Documentation

```
swagger localhost:8000/swagger
```