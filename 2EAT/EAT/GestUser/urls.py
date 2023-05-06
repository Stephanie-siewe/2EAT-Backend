from django.urls import path,include
from rest_framework.routers import SimpleRouter

from .views import *
router = SimpleRouter()
router.register('users', UserViewSet, 'users')
urlpatterns = [
path('validity', VerifyTokenValidity),
path('registration', UserCreate.as_view()),
path('login', UserLoginView.as_view()),
path('logout',UserLogOutView.as_view()),
path('user/changeimage', UserChangeProfileImage.as_view()),
path('user/changeinfo', UserChangeInformation.as_view()),
]+router.urls
