# Generated by Django 3.0.3 on 2020-02-20 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_viewsquantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='subgenre',
            field=models.CharField(choices=[('Popular science', 'Научпоп'), ('Self-development', 'Саморазвитие')], max_length=20, null=True),
        ),
    ]
