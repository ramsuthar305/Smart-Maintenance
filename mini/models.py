from django.db import models



# Create your models here.
class maintenance(models.Model):
    image=models.ImageField(upload_to='static/')
