 # This is an example configuration file for the prod
 # environment. This file should never be committed to git.

#This should be replaced by a proper secret.
SECRET_KEY = ''

STATIC_ROOT = '/var/www/spork.no/band/static/'

ALLOWED_HOSTS = [
    'band.spork.no'
]

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'band_booking',
    'USER': 'band_booking',
    'PASSWORD': '',
    'HOST': 'localhost',
    'PORT': '',
    }
}
