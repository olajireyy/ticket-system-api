## Create Directory
- mkdir Eventure
- cd Eventure

## Activate env
- virtualenv venv or python -m venv venv
- venv/Scripts/activate or cd venv/Scripts & activate
- cd ../../

## Install dependencies with pip
- pip install django djangorestframework ...

 ## Create Project in root
 - django-admin start project config .
 ## create app
 - python manage.py startapp events

## Settings
- Add installed apps to INSTALLED APPS
- Configure database
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ticket_api',      # The database name you created
        'USER': 'postgres',        # The default postgres user
        'PASSWORD': '', # The password you set during installation
        'HOST': 'localhost',
        'PORT': '5432',
        }
    }
- Make migrations
    - python manage.py makemigrations
    - python manage.py migrate

    
## Redis
  -  CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1", # The /1 is the Redis database number
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }