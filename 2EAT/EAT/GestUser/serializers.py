from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.conf import settings
import base64
import io
User = CustomUser

#Methode pour creer une image de profil par defaut
# def create_default_profile_image():
#     with open('static/images/default-profile-image.png', 'rb') as f:
#         image_data = f.read()
#         print('Image_data',image_data)
#         image_data_b64 = base64.b64encode(image_data)
#         return io.BytesIO(base64.b64decode(image_data_b64))

#User creation serializer
class CustomUserSerializer(serializers.ModelSerializer):
    #profile_image = serializers.CharField(required=False, default=None)

    #     def create(self, validated_data):
        """
        # la methode valid_data.pop recupere l'image de profil et renvoi None s'il n'existe pas
        profile_image = validated_data.pop('profile_image', None)
        #user = User.objects.create_user(**validated_data)
        user = super().create(validated_data)
        if profile_image:
            #user.profile_image = profile_image
            user.profile_image.save(profile_image.name, profile_image)

        else:
            image_prof = create_default_profile_image()
            #user.profile_image = 'default_profile_image.png'
            user.profile_image.save(image_prof.name,image_prof)

        #user.save()

        return user
        """
        #defined a creations's fields of user
        class Meta:
            model = CustomUser
            fields = ['id', 'username', 'email', 'password', 'profile_image', 'phone_number']
            extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            profile = validated_data.pop('profile_image', None)
            print('Profile image type',profile)

            # if profile == None :
            #     profile = create_default_profile_image()

            #Create user
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                profile_image=validated_data.get('profile_image'),
                phone_number=validated_data.get('phone_number')
            )
            return user

class UserChangePassword(serializers.Serializer):
    password = serializers.CharField()


#Change Profile image of user serializer
class UserChangeProfileImage(serializers.Serializer):
    profile_image = serializers.CharField(max_length=1000)
    id = serializers.CharField()

#Change Infos User Serializer
class UserChangeInfos(serializers.Serializer):
    phone_number = serializers.CharField(max_length=9)
    username = serializers.CharField()
    email = serializers.EmailField()
    id = serializers.CharField()

