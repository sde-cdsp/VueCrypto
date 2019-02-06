## Project setup

This project works with Django as a backend and VueJS as the frontend. Django is almost exclusively sending data as JSON (such as the user connected, cryptocurrencies infos...), whereas Vue handle them.

## VueJS part

### in mycryptolist directory:
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

## Django part

### in VueCrypto/settings.py

- install postgresql
- Create a postgresql database for this project
- Change the DATABASES settings relatively. See https://docs.djangoproject.com/en/2.1/ref/settings/#databases

### 

### In root directory:

Apply django migrations to populate the database:
```
python manage.py migrate
```

Run localhost server on port 8000:
```
python manage.py runserver
```

You are good to go

