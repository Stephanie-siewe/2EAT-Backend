from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from GestUser.models import CustomUser

# Create your views here

User=CustomUser
class PlaceCreate(APIView):
    serializer_class = PlaceSerializer

    def post(self, request):
       user_id = request.data.get('user_id')
       name = request.data.get('name')
       category_id = request.data.get('category_id')
       order = request.data.get('order')
       description = request.data.get('description')
       city = request.data.get('city')
       quarter = request.data.get('quarter')
       longitude = request.data.get('longitude')
       latitude = request.data.get('latitude')
       picture = request.data.get('picture')



       if not user_id:
           content={"error": "Any user id"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

       if not category_id:
           content = {"error": "Any category id"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

       if not name:
           content = {"error": "Any name"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

       if not order:
           order = False
       elif order == "true":
           order = True
       else:
           order = False
       if not picture:
           content = {"error": "Any picture to describe your place"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

       if not quarter:
           content = {"error": "Any quarter entry"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

       if not city:
           content = {"error": "Any city"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

       if not longitude:
           content = {"error": "Any longitude"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

       if not latitude:
           content = {"error": "Any latitude"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

       try:
           user = User.objects.get(id=user_id)
           category = Category.objects.get(id=category_id)
           localisation = Localisation()


           localisation.city = city
           localisation.quarter = quarter
           localisation.latitude = latitude
           localisation.longitude = longitude

           try:

               if not Localisation.objects.filter(longitude=longitude,latitude=latitude).exists():
                   localisation.save()


                   try:
                       binary_image = picture.read()
                       place = Place()
                       place.localisation = localisation
                       place.name = name
                       place.order = order
                       place.user = user
                       place.description = description
                       place.picture = binary_image
                       place.category = category
                       place.save()


                       content = {'success':'place registred!!!'}
                       return Response(content, status=status.HTTP_201_CREATED)
                   except Exception as e:
                       print('exception place',str(e))
                       content = {'error': 'impossible to create a place'}
                       return Response(content, status=status.HTTP_400_BAD_REQUEST)
               else:
                   content = {'error': 'this localisation already exists'}
                   return Response(content, status=status.HTTP_400_BAD_REQUEST)
           except Exception as exc:
               print('exception',str(exc))
               content = {'error': 'impossible to create a localisation'}
               return Response(content, status=status.HTTP_400_BAD_REQUEST)



       except:
           content = {"error": "This User or this category does not exist"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.select_related().all()
    serializer_class = PlaceSerializerList


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    print('queryset',queryset)
    serializer_class = CategorySerializer




