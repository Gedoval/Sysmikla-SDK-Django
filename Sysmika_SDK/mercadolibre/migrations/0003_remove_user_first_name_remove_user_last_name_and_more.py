# Generated by Django 4.0 on 2022-01-03 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mercadolibre', '0002_remove_user_access_token_user_app_id_user_app_secret'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='mercadolibre.accesstoken'),
        ),
        migrations.AlterField(
            model_name='user',
            name='app_id',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='user',
            name='app_secret',
            field=models.CharField(max_length=500),
        ),
    ]