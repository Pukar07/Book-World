# Generated by Django 3.2.8 on 2022-03-03 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.CharField(max_length=200, null=True),
        ),
    ]