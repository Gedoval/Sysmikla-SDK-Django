# Generated by Django 4.0.1 on 2022-01-23 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercadolibre', '0004_remove_user_access_token_user_redirect_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='app_token',
            field=models.CharField(default='', max_length=600),
        ),
        migrations.AddField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(default='', max_length=600),
        ),
    ]
