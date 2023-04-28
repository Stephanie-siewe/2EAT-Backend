from rest_framework import serializers
from .models import *
from GestUser.serializers import  CustomUserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')

class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = ['id','city','quarter','longitude','latitude']


        def create(self,validated_data):
            return Localisation.objects.create(**validated_data)

class PlaceSerializerList(serializers.ModelSerializer):
    localisation = LocalisationSerializer()
    category = CategorySerializer()
    user = CustomUserSerializer()


    class Meta:
        model = Place
        fields = ['id', 'category', 'localisation', 'user', 'order', 'name', 'description', 'picture']
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



class DishSerializer(serializers.ModelSerializer):
    pass










