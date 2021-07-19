from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=120)
    password = models.CharField(max_length=300)
    account  = models.CharField(max_length=50, null=True)
    name     = models.CharField(max_length=50, null=True)
    phone    = models.CharField(max_length=50, null=True)
    
    class Meta:
        db_table = 'users'


class ProfilePhoto(models.Model):
    user      = models.ForeignKey('User', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)

    class Meta:
        db_table = 'profile_photos'