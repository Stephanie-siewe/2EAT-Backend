# Generated by Django 4.1.7 on 2023-04-25 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('picture', models.BinaryField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('specifity', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Localisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(max_length=35)),
                ('longitude', models.FloatField(max_length=35)),
                ('city', models.CharField(max_length=50)),
                ('quarter', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('order', models.BooleanField()),
                ('description', models.TextField()),
                ('picture', models.BinaryField(blank=True, null=True)),
                ('localisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestPlace.localisation')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConstituentDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price_U', models.FloatField()),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestPlace.dish')),
            ],
        ),
    ]
