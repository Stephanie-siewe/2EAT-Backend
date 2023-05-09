import re
from datetime import datetime, timedelta

import pytz
from django.utils import timezone
from rest_framework.authtoken.models import Token

from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework.views import APIView
from .models import *
import base64

#CustomerUser is a new model user known by django
User=CustomUser


def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None
#Api view for user creation
class UserCreate(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            username = request.data.get('username')
            email = request.data.get('email')

            # verify if the username already exist
            try:

                user = CustomUser.objects.get(username=username)
                content = {'error': 'This Username Already Exists.'}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
            except CustomUser.DoesNotExist:
                pass
            #verify if the email already exist
            try:
                user = CustomUser.objects.get(email=email)
                content = {'error': 'This Email Already Exists.'}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
            except CustomUser.DoesNotExist:
                pass


            # Take image downloaded
            profile_image = request.data.get('profile_image')


            #Save User with your profile-image
            user = serializer.save()

            # Save profile image
            if profile_image:
                # convertir l'image en binaire
                binary_image = base64.b64decode(profile_image)
                user.profile_image = binary_image
                #save user
                user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Api view for Login
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("password",password)
        #Verify if the user enterred a mail
        if '@' in username:
            try:
                #verify if the mail exists
                user = CustomUser.objects.get(email=username)
                username = user.username
                print("username",username)
            except CustomUser.DoesNotExist:
                content = {'error': 'User with this email does not exist.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        #Verify if teh user enterred a username
        try:
            #verify if the username exists
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None
        # user = authenticate(username=username, password=password)
        #verify if the password is the user's password
        if user:
            rep = user.check_password(password)
            print('rep',rep)
            if rep:
                #create or get the token of the user
                token,created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
            else:
                content = {'error': 'Invalid password.'}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        else:
            content = {'error': 'User with this username does not exist.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def VerifyTokenValidity(request):
    tok = request.data.get('token')
    token = Token.objects.get(key=tok)
    print('token', token)
    dat = datetime.now()
    date_actual_with_timezone = dat.replace(tzinfo=pytz.UTC)
    if date_actual_with_timezone - token.created > timedelta(days=30):
        is_expired = True
    else:
        is_expired = False
    return Response(is_expired)

#Api view for Logout
class UserLogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        #delete the token of the user
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

#Api view which permit to list a users and to see a details of one user
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



def changePassword(self, request):
    pass


#Api view for change Profile Image
class UserChangeProfileImage(APIView):
    serializer_class = UserChangeProfileImage
    def post(self,request):

            id = request.data.get('id')
            profile_image = request.data.get('profile_image')
            print('profile',profile_image)
            print('id', id)

            try:
                user = CustomUser.objects.get(id=id)
                # binary_image = base64.b64decode(profile_image)
                # if isinstance(profile_image, bytes):
                #     binary_image = profile_image
                #
                # else:
                #     binary_image = profile_image.read()
                #     print('binary', binary_image)
                #     print('type 1', type(binary_image))
                #     print('type 2', type(base64.b64decode(binary_image)))
                binr = profile_image.encode('utf-8')
                binary_image = base64.b64decode(binr)
                user.profile_image = binary_image
                user.save()
                content = {'success': 'Profile image updated'}
                return Response(content, status=status.HTTP_202_ACCEPTED)
            except CustomUser.DoesNotExist:
                content = {'error': 'User with this username does not exist.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            content = {'error': 'data missed,please retry'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

class UserChangeInformation(APIView):
    serializer_class = UserChangeInfos

    def post(self, request):
        id_user = request.data.get("id")
        email = request.data.get("email")
        username = request.data.get("username")
        phone_number = request.data.get("phone_number")

        print('username',username)
        print('typeofusername', type(username))
        print('email', email)
        if id_user==None :
            content = {'error': 'Any id sent'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if username==None or username =='':
            content = {'error': 'Username is required'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if email == None or email == '':
            content = {'error': 'Email is required'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        if validate_email(email) == False:
            content = {'error': 'Email is not valid'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            user = CustomUser.objects.get(email=email)
            if str(user.id) != id_user:
                content = {'error': 'This Email already exists '}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            # exception if user is not exist
            pass

        try:
            user = CustomUser.objects.get(username=username)
            if str(user.id) != id_user:
                content = {'error': 'This username already exists '}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            # exception if user is not exist
            pass




        try:
            user = CustomUser.objects.get(id=id_user)
            user.phone_number = phone_number
            user.username = username
            user.email = email
            user.save()
            content = {'success': 'Informations modified'}
            return Response(content, status=status.HTTP_202_ACCEPTED)

        except CustomUser.DoesNotExist:
            content = {'error': 'User Not Found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)










