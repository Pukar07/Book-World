# Generated by Django 3.2.8 on 2022-03-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0004_auto_20220315_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='ward_no',
            field=models.IntegerField(null=True),
        ),
    ]