# Generated by Django 4.0 on 2022-01-02 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=500)),
                ('token_type', models.CharField(max_length=100)),
                ('expires_in', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=-1)),
                ('refresh_token', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='FirstName')),
                ('last_name', models.CharField(max_length=100, verbose_name='LastName')),
                ('meli_id', models.IntegerField(default=-1)),
                ('sysmika_id', models.IntegerField(default=-1)),
                ('access_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mercadolibre.accesstoken')),
            ],
        ),
        migrations.CreateModel(
            name='RealState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('successful', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=2000)),
                ('publication_id', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mercadolibre.user')),
            ],
        ),
    ]
