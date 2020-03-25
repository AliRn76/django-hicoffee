from rest_framework import serializers
from app.models import Item

class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model   = Item
        fields  = ['imageUrl', 'name', 'category', 'description', 'number', 'price']
