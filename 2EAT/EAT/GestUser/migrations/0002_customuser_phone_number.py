# Generated by Django 4.1.7 on 2023-04-25 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestUser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]