from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class CustomUser(AbstractUser):
    app_label = 'GestUser'
    profile_image = models.BinaryField(blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set'  # change the related_name to avoid the clash
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set'  # change the related_name to avoid the clash
    )
