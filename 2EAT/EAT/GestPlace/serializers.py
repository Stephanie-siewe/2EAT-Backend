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
        extra_kwargs = {'category': {'read_only': True}, 'user': {'read_only': True}, 'localisation': {'read_only': True}}

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
    place = PlaceSerializerList()

    class Meta:
        model = Dish
        fields = '__all__'
        extra_kwargs = {'place': {'read_only': True}}


class DishCreateSerializer(serializers.Serializer):
    place = serializers.CharField(max_length=20)
    price = serializers.FloatField(default=0)
    name = serializers.CharField(max_length=40)
    # specifity = serializers.JSONField()
    picture = serializers.ImageField()



class ConstituentCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    dish = serializers.CharField(max_length=30)
    price_u = serializers.FloatField(default=0)




class ModifyPictureSerializer(serializers.Serializer):
    picture = serializers.ImageField()
    object_id = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()


    class Meta:
        model = Comments
        fields = '__all__'
    def get_replies(self,obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return None


class CommentLikeSerializer(serializers.ModelSerializer):

    #user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommentLike
        fields = '__all__'
