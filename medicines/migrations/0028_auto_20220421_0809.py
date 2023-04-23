# Generated by Django 3.2.8 on 2022-04-21 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0027_auto_20220420_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='pres',
            field=models.ImageField(blank=True, default='', null=True, upload_to='medicines/prescription'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='ward_no',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='zip_code',
            field=models.IntegerField(max_length=50, null=True),
        ),
    ]