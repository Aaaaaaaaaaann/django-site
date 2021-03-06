# Generated by Django 3.0.3 on 2020-02-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('activated', models.BooleanField(default=False)),
                ('joined', models.DateField(blank=True, null=True)),
                ('unsubscribed', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
