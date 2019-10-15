from djangoweb.celery import app
from djangoweb.library.Main import Publish
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from djangoweb.library.GenerateKey import key

@app.task
def runscript():
    encoded = User.objects.filter(is_superuser=True)[1].first_name.encode()
    f = Fernet(key)
    decrypted = f.decrypt(encoded)
    decoded = decrypted.decode()
    print('hello')
    Publish(decoded)