# Generated by Django 3.2.8 on 2022-04-04 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0007_auto_20220404_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.CharField(max_length=20, null=True),
        ),
    ]