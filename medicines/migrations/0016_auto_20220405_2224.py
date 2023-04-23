# Generated by Django 3.2.8 on 2022-04-05 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0015_rename_pres_shippingaddress_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='image',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='pres',
            field=models.ImageField(blank=True, default='', null=True, upload_to='medicines/prescription'),
        ),
    ]