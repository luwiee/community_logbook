# Generated by Django 4.0.3 on 2022-03-31 03:36

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
            name='log_info',
            fields=[
                ('name', models.CharField(default='main', max_length=10, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='none', max_length=255)),
                ('name', models.CharField(default='NULL', max_length=255)),
                ('destination', models.CharField(default='NULL', max_length=255)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('staff', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]