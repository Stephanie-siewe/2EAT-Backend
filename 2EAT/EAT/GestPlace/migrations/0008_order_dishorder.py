# Generated by Django 4.1.7 on 2023-05-04 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GestPlace', '0007_alter_commentlike_is_like_placenote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('En cours', 'En cours'), ('Livre', 'Livre'), ('Annule', 'Annule')], max_length=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField(default=0)),
                ('dish', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='GestPlace.dish')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DishOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte', models.IntegerField(default=0)),
                ('constituent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='GestPlace.constituentdish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestPlace.order')),
            ],
        ),
    ]
