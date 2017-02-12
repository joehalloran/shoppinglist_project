from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*', '.shopping-list-auth.appspot.com', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shoppinglist',
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASSWORD'],
    }
}
# In the flexible environment, you connect to CloudSQL using a unix socket.
# Locally, you can use the CloudSQL proxy to proxy a localhost connection
# to the instance
DATABASES['default']['HOST'] = '/cloudsql/shopping-list-auth:us-central1:shopping-list-auth-sql'
if os.getenv('GAE_INSTANCE'):
    pass
else:
    DATABASES['default']['HOST'] = '127.0.0.1'

STATIC_URL = 'https://storage.googleapis.com/shopping-list-auth-static/static/'