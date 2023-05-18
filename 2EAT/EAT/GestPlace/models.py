from django.core.validators import MinValueValidator, MaxValueValidator
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
    price = models.FloatField(default=0)
    # specifity = models.JSONField()
    place = models.ForeignKey(Place,on_delete=models.CASCADE)


class ConstituentDish(models.Model):
    name = models.CharField(max_length=50)
    price_U = models.FloatField()
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)



class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    parent = models.ForeignKey('self',  on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    comment =models.ForeignKey(Comments, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} {self.comment} {self.is_like}'


class PlaceNote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    note = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(choices=(('En cours', 'En cours'), ("Livre", "Livre"), ('Annule', 'Annule')), max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0)

    def update_status(self, new_status):
        self.status = new_status
        self.save()


class DishOrder(models.Model):
    constituent = models.ForeignKey(ConstituentDish, on_delete=models.SET_NULL, null=True)
    qte = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
