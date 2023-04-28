
from django.urls import path,include
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import *
from .views import PlaceCreate

router = DefaultRouter()
router.register('view', PlaceViewSet)
router.register('categorie', CategoryViewSet)
urlpatterns = [
path('add', PlaceCreate.as_view())
# path('listP',CategoryListAPIview.as_view())
]+router.urls