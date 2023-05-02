
from django.urls import path,include
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import *
from .views import PlaceCreate

router = DefaultRouter()
router.register('placesimple', PlaceViewSet)
router.register('categorie', CategoryViewSet)
router.register('dishsimple', DishViewSet)
urlpatterns = [
path('add/place', PlaceCreate.as_view()),
path('add/dish', DishCreate.as_view()),
path('add/consti', AddConstituent.as_view()),
path('update/place', ModifyPlaceInformations.as_view()),
path('update/consti', ModifyConstituent.as_view()),
path('update/dish/', ModifyDish.as_view()),
path('update/place/photo', ModifyPicturePlace.as_view()),
path('update/dish/photo', ModifyPictureDish.as_view()),
path('searchbylocal/<str:long>/<str:lati>', SearchPlaceByLocalisation.as_view()),
path('add/comment', CommentCreate.as_view()),
path('comments', CommentsList.as_view()),
path('comments/<int:id>', CommentsDetail.as_view()),
path('comments/<int:pk>/<int:userid>/like', CommentLikeToggle.as_view()),
path('comments/<int:pk>/likes-count', CommentLikesCount.as_view()),
path('noteplace/<int:userid>/<int:pk>/<int:note>', NotePlace.as_view()),

path('delete/place/<int:pk>', PlaceDelete.as_view()),
path('delete/dish/<int:pk>', DishDelete.as_view()),
path('delete/consti/<int:pk>', ConstituentDishDelete.as_view())
]+router.urls
