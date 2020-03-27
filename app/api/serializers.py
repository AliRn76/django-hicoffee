from rest_framework import serializers
from app.models import Item

class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model   = Item
        fields  = ['image_url', 'name', 'category', 'description', 'number', 'price']


class CreateItemSerializers(serializers.ModelSerializer):
    class Meta:
        model   = Item
        fields  = ['name', 'category', 'description', 'number', 'price']

