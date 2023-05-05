
import math
from operator import itemgetter
from statistics import mean

from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from GestUser.models import CustomUser

# Create your views here

User=CustomUser


#Create a place
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


           if Localisation.objects.filter(longitude=longitude).filter(latitude=latitude).exists() == True:
               localisation = Localisation.objects.filter(longitude=longitude).filter(latitude=latitude)[0]

           else:
               localisation = Localisation()

               localisation.city = city
               localisation.quarter = quarter
               localisation.latitude = latitude
               localisation.longitude = longitude

               try:
                   localisation.save()
               except Exception as exc:
                   print('exception', str(exc))
                   content = {'error': 'impossible to create a localisation'}
                   return Response(content, status=status.HTTP_400_BAD_REQUEST)

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

               content = {'success': 'place registred', 'id': place.id}
               return Response(content, status=status.HTTP_201_CREATED)
           except Exception as e:
               print('exception place', str(e))
               content = {'error': 'impossible to create a place'}
               return Response(content, status=status.HTTP_400_BAD_REQUEST)



       except:
           content = {"error": "This User or this category does not exist"}
           return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

#list all places and see details of a place without theirs dishes
class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.select_related().all()
    serializer_class = PlaceSerializerList


class ModifyPlaceInformations(APIView):
    serializer_class = PlaceSerializer

    def post(self, request):
        name = request.data.get('name')
        order = request.data.get('order')
        description = request.data.get('description')
        category_id = request.data.get('category_id')
        # I'm tired, the justifications are in the modifications of the other models
        place_id = request.data.get('user_id')
        city = request.data.get('city')
        quarter = request.data.get('quarter')
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')

        if not place_id:
            content = {"error": "Any place id"}
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
            place = Place.objects.get(id=place_id)
            category = Category.objects.get(id=category_id)




            if Localisation.objects.filter(longitude=longitude).filter(latitude=latitude).exists() == True:
                localisation = Localisation.objects.filter(longitude=longitude).filter(latitude=latitude)[0]

            else:
                localisation = Localisation()
                localisation.city = city
                localisation.quarter = quarter
                localisation.latitude = latitude
                localisation.longitude = longitude

                try:
                    localisation.save()
                except Exception as exc:
                    print('exception', str(exc))
                    content = {'error': 'impossible to create a localisation'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

            try:
                place.localisation = localisation
                place.name = name
                place.order = order
                place.description = description
                place.category = category
                place.save()

                content = {'success': 'place modified', 'id': place.id}
                return Response(content, status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                print('exception place', str(e))
                content = {'error': 'impossible to modify a place'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)



        except:
            content = {"error": "This place or this category does not exist"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


class ModifyPicturePlace(APIView):
    serializer_class = ModifyPictureSerializer

    def post(self, request):
        place_id = request.data.get('object_id')
        picture = request.data.get('picture')

        if not picture:
            content = {"error": "field picture empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not place_id:
            content = {"error": "field id empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


        if Place.objects.filter(id=place_id).exists() == True:
            place = Place.objects.filter(id=place_id)[0]
            place.picture = picture.read()
            place.save()
            content = {"success": "Modified"}
            return Response(content, status=status.HTTP_202_ACCEPTED)

        else:
            content = {"error": "place does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)



#list all Categories and see details of a category
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    print('queryset',queryset)
    serializer_class = CategorySerializer



#create a dish
class DishCreate(APIView):
    serializer_class = DishCreateSerializer

    def post(self, request):
        name = request.data.get('name')
        price = request.data.get("price")
        place = request.data.get('place')
        picture = request.data.get('picture')


        if not picture:
            content = {"error": "Any picture to describe your place"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not price:
            price = 0

        if float(price) < 0:
            content = {"error": "Enter a greater price than 0"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not place:
            content = {"error": "Your Dish is not a food of a Place"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not name:
            content = {"error": "Please give a name of your dish"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


        try:
            place_info = Place.objects.get(id=place)
            dish = Dish()
            dish.name = name
            dish.picture = picture.read()
            dish.place = place_info
            dish.price = price

            dish.save()

            content = {"success": "Dish Created","id":dish.id}
            return Response(content, status=status.HTTP_201_CREATED)


        except Exception as e:
            print("exception", e)
            content = {"error": "Place does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

#list all dishes and see details of a dish without theirs constituents
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

#modify dish of a place
class ModifyDish(APIView):
    serializer_class = DishCreateSerializer

    def post(self, request):
        picture = None
        name = request.data.get('name')
        price = request.data.get('price')
        #Here place represents a dish id , yes it's weird but ...
        place = request.data.get('place')

        if not name:
            content = {"error": "field name empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not price:
            content = {"error": "field price empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not place:
            content = {"error": "any dish id"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            dish = Dish.objects.get(id=place)
            dish.name = name
            dish.price = price
            dish.save()
            content = {"success": "Modified", "dish": {"id": dish.id, "name": dish.name, "price":dish.price, "place":dish.place.id}}
            return Response(content, status=status.HTTP_202_ACCEPTED)

        except:
            content = {"error": "this dish does not exists empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


#modify a picture of a dish
class ModifyPictureDish(APIView):
    serializer_class = ModifyPictureSerializer

    def post(self, request):
        dish_id = request.data.get('object_id')
        picture = request.data.get('picture')

        if not picture:
            content = {"error": "field picture empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not dish_id:
            content = {"error": "field id empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if Dish.objects.filter(id=dish_id).exists() == True:
            place = Place.objects.filter(id=dish_id)[0]
            place.picture = picture.read()
            place.save()
            content = {"success": "Modified"}
            return Response(content, status=status.HTTP_202_ACCEPTED)

        else:
            content = {"error": "Dish does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)




#add a constituent of a dish
class AddConstituent(APIView):
    serializer_class = ConstituentCreateSerializer

    def post(self, request):
        price_u = request.data.get('price_u')
        name = request.data.get('name')
        dish = request.data.get('dish')

        if not price_u:
            content = {"error": "field price empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not dish:
            content = {"error": "field dish empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not name:
            content = {"error": "Any name to describe your constituent"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        constituent = ConstituentDish()

        try:
            dish_info = Dish.objects.get(id=dish)
            constituent.name = name
            constituent.price_U = price_u
            constituent.dish = dish_info
            constituent.save()

            content = {"success": "Constituentof Dish saved", "id": constituent.id}
            return Response(content, status=status.HTTP_201_CREATED)


        except Dish.DoesNotExist:
            content = {"error": " Dish does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

#Modify a constituent of a dish

class ListConstituent(viewsets.ModelViewSet):
    queryset = ConstituentDish.objects.all()
    serializer_class = ConstituentSerializer
class ModifyConstituent(APIView):
    serializer_class = ConstituentCreateSerializer

    def post(self, request):
        name = request.data.get("name")
        price_u = request.data.get("price_u")
    # I use the same serializer to create and to update a Constituent
    # I know it's weird but I am tired and I'm running out of time
        constituent_id = request.data.get("dish")

        if not price_u:
            content = {"error": "field price empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not name:
            content = {"error": "field name empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not constituent_id:
            content = {"error": "field constituent id  empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            constituent = ConstituentDish.objects.get(id=constituent_id)
            constituent.name = name
            constituent.price_U = price_u
            constituent.save()

            content = {"success": "Modified", "constituent":{"id":constituent_id,"name":constituent.name, "price_U": constituent.price_U, "dish": constituent.dish.id} }
            return Response(content, status=status.HTTP_202_ACCEPTED)

        except Exception as erro:
            print('error',erro)
            content = {"error": "Constituent does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)



#calculation of the geodesic distance between 2 points
def distance(lat1, lon1, lat2, lon2):
    r = 6371  # rayon moyen de la Terre en kilomètres

    # conversion des latitudes et longitudes en radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # calcul de la distance
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    d = r * c

    return d


class SearchPlaceByLocalisation(APIView):

    def get(self, request, long, lati):
        userLongitude = float(long)
        userLatitude  = float(lati)
        nearPlace = []

        places = Place.objects.select_related().all()

        for place in places:

            dist = distance(userLatitude, userLongitude, place.localisation.latitude, place.localisation.longitude)
            dico = {"place_id": place.id, "distance": dist}
            nearPlace.append(dico)

        response = sorted(nearPlace, key=itemgetter('distance'))
        print('response', response)
        content = {"response": response}
        return Response(content,  status=status.HTTP_200_OK)



class CommentCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CommentsList(generics.ListCreateAPIView):
    queryset = Comments.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer

class CommentsDetail(generics.RetrieveAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'



class CommentLikeToggle(APIView):
    queryset = Comments.objects.all()
    serializer_class = CommentLikeSerializer

    def get(self, request, pk,userid, *args, **kwargs):
        # print('pk',pk)
        try:

            comment = Comments.objects.get(id=pk)
            user = CustomUser.objects.get(id=userid)
            comment_like, created = CommentLike.objects.get_or_create(user=user, comment=comment)
            if not created:
                comment_like.delete()

                likes_count = CommentLike.objects.filter(comment=pk).count()
                content = {"message": "Like removed", "likes": likes_count}
                return Response(content, status=status.HTTP_204_NO_CONTENT)
            likes_count = CommentLike.objects.filter(comment=pk).count()
            content = {"message": "like added", "likes": likes_count}

            return Response(content, status=status.HTTP_201_CREATED)
        except:
            content = {"error": "Comment or User does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

class CommentLikesCount(generics.RetrieveAPIView):
    queryset = Comments.objects.all()

    def get(self, request, pk, *args, **kwargs):
        try:
            comment = Comments.objects.get(id=pk)
            likes_count = CommentLike.objects.filter(comment=pk).count()
            return Response({"likes": likes_count}, status=status.HTTP_200_OK)
        except Exception as e:
            print("exception:", e)
            content = {"error": "Comment does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)




class NotePlace(APIView):
    # queryset = PlaceNote.objects.all()

    def get(self, request, userid, pk, note, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=userid)
            place = Place.objects.get(id=pk)

            if note>=0 and note<6:
                note_place, created = PlaceNote.objects.get_or_create(user=user, place=place)
                if note != note_place.note:
                    note_place.note = note
                    note_place.save()

                notes = []
                queryset = PlaceNote.objects.filter(place=pk)
                for i in queryset:
                    notes.append(i.note)
                moy = mean(notes)
                content = {"success": "note changed", "moy": moy}
                return Response(content, status=status.HTTP_200_OK)


            else:
                content = {"error":"this note is not valid"}
                return Response(content,status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            print('error',e)
            content = {"error": "this user or this place does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)



class PlaceDelete(generics.DestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializerList
    lookup_field = 'pk'

class DishDelete(generics.DestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    lookup_field = 'pk'

class ConstituentDishDelete(generics.DestroyAPIView):
    queryset = ConstituentDish.objects.all()
    serializer_class = ConstituentSerializer
    lookup_field = 'pk'


class OrderAPIView(APIView):
    def post(self, request, *args, **kwargs):

        dish = request.data.get('dish')
        user = request.data.get('user')

        print('data', request.data)
        try:

            dish = Dish.objects.get(id=dish)
            user = CustomUser.objects.get(id=user)
            price = dish.price
            data = {'user': user.id, 'dish': dish.id, 'price': price, 'status': 'En cours'}
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {"error": "this dish or user does not exist"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

class ChangeStatusOrder(APIView):
    def get(self, request,id, stat, *args, **kwargs):
        print('id',id)
        try:
            order = Order.objects.get(id=id)

            if stat == 1:
                order.status = 'Livre'
                order.save()
                content = {"success": "status changed"}
                return Response(content, status=status.HTTP_202_ACCEPTED)
            if stat == 2:
                order.status = 'Annule'
                order.save()
                content = {"success": "status changed"}
                return Response(content, status=status.HTTP_202_ACCEPTED)
            else:
                content = {"error": "Status is not acceptable"}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            content = {"error":"Order does not exists"}
            return  Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


class OrderDelete(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'




class GetPlacesByCategoryId(generics.ListAPIView):
    serializer_class = PlaceSerializerList

    def get_queryset(self):
        id = self.kwargs['id']
        queryset = Place.objects.filter(category__id=id)
        return queryset


class GetDishesByPlaceId(generics.ListAPIView):
    serializer_class = DishSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        queryset = Dish.objects.filter(place__id=id)
        return queryset


class GetConstituentByDishId(generics.ListAPIView):
    serializer_class = ConstituentSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        queryset = ConstituentDish.objects.filter(dish__id=id)
        return queryset


class DishOrderAPIView(APIView):


    def post(self, request):
        id_order = request.data.get('order')
        id_consti = request.data.get('consti')
        qte = request.data.get('qte')

        if not qte:
          qte = 0
        if not id_order:
            content = {"error": "field order is empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not id_consti:
            content = {"error": "field consti empty"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            order = Order.objects.get(id=id_order)
            constit = ConstituentDish.objects.get(id=id_consti)
            if constit.dish.id != order.dish.id:

                content = {"error": "it is not a constituent of this dish"}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                print('broo', DishOrder.objects.all())
                created = DishOrder.objects.filter(order=order, constituent=constit).exists()
                print('created', created)

                price = constit.price_U * qte
                order.price = order.price + price
                order.save()








        except Exception as e:
            print('exception :', e)
            content = {"error": "this order or constituent does not exists"}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)


