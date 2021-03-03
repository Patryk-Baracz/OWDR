# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# set name, user and password

DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'password',
    }
}
