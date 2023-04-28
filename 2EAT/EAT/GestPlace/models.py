from django.db import models
from GestUser.models import CustomUser
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

class Localisation(models.Model):
    latitude = models.FloatField(max_length=35)
    longitude = models.FloatField(max_length=35)
    city = models.CharField(max_length=50)
    quarter = models.CharField(max_length=50)

    class Meta:
        unique_together = ('longitude', 'latitude',)


class Place(models.Model):
    name = models.CharField(max_length=40)
    order = models.BooleanField()
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    picture = models.BinaryField(blank=True, null=True)
    localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)



class Dish(models.Model):
    name = models.CharField(max_length=50)
    picture = models.BinaryField(blank=True, null=True)
    price = models.FloatField()
    specifity = models.JSONField()
    place = models.ForeignKey(Place,on_delete=models.CASCADE)


class ConstituentDish(models.Model):
    name = models.CharField(max_length=50)
    price_U = models.FloatField()
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)



