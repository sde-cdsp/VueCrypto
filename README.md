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

### Database configuration

- install postgresql
- Create a postgresql database for this project
- In *VueCrypto/settings.py*,Change the DATABASES settings relatively. See https://docs.djangoproject.com/en/2.1/ref/settings/#databases

### specific configs

A *configs.sample.py* file is provided. You must set the provided variables to have a working configuration.
When this is done, the file must be renamed *configs.py*

### In root directory:

Apply django migrations to populate the database:
```
python manage.py migrate
```

Run localhost server on port 8000:
```
python manage.py runserver
```

You are good to go !

