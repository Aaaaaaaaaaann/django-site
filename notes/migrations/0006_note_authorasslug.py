# Generated by Django 3.0.3 on 2020-03-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_auto_20200227_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='authorAsSlug',
            field=models.SlugField(null=True),
        ),
    ]
