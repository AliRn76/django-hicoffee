from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Item(models.Model):
    id          = models.AutoField(db_column='ID', primary_key=True)
    imageUrl    = models.ImageField(db_column="imageUrl", upload_to='images/', max_length=256)
    name        = models.CharField(db_column='Name', max_length=128, null=True)
    category    = models.CharField(db_column='Category', max_length=128, null=True)
    description = models.CharField(db_column='Description', max_length=256,  blank=True, null=True)
    number      = models.IntegerField(db_column='Number', null=True)
    price       = models.IntegerField(db_column='Price', null=True)

    class Meta:
        db_table = 'Item'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)