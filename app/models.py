from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Item(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=128, blank=True, null=True)
    category = models.CharField(db_column='Category', max_length=128, blank=True, null=True)
    description = models.CharField(db_column='Description', max_length=256,  blank=True, null=True)
    number = models.IntegerField(db_column='Number', blank=True, null=True)
    price = models.IntegerField(db_column='Price', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Item'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)