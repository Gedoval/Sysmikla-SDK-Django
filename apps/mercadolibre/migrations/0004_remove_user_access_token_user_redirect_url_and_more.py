# Generated by Django 4.0.1 on 2022-01-08 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercadolibre', '0003_remove_user_first_name_remove_user_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='access_token',
        ),
        migrations.AddField(
            model_name='user',
            name='redirect_url',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.DeleteModel(
            name='AccessToken',
        ),
    ]