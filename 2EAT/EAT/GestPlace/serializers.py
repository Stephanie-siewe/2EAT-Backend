from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ('__all__')

class LocalisationSerializer(serializers.Serializer):
    class Meta:
        model = Localisation
        fields = ['id','city','quarter','longitude','latitude']


        def create(self,validated_data):
            return Localisation.objects.create(**validated_data)

class PlaceSerializerList(serializers.Serializer):
    class Meta:
        model = Place
        fields = ['id', 'category_id', 'localisation_id', 'user_id', 'order', 'name', 'description', 'picture']
        # fields = ('__all__')

class PlaceSerializer(serializers.Serializer):
   user_id = serializers.CharField(max_length=50)
   name = serializers.CharField(max_length=50)
   order = serializers.BooleanField()
   picture = serializers.ImageField()
   description = serializers.CharField(max_length=255)
   category_id = serializers.CharField(max_length=20)
   city = serializers.CharField(max_length=50)
   quarter = serializers.CharField(max_length=50)
   longitude = serializers.CharField(max_length=35)
   latitude = serializers.CharField(max_length=35)











