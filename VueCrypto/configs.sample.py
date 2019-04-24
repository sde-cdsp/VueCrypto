import os

SECRET_KEY = 'your_secret_key'
DB_USER = 'your_user'
DB_PWD = 'your_password'
DB_NAME = 'db_name'
DB_PORT = '5432'
DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
DB_HOST = ''


CMC_KEY = 'your_cmc_api_key'
CMC_DOMAIN = 'https://pro-api.coinmarketcap.com/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your e-mail address"
EMAIL_HOST_PASSWORD = "your email password"


for k, v in os.environ.items():
    if k.startswith("DOCKER_"):
        key = k.split('_', 1)[1]
        locals()[key] = str(v)