# Generated by Django 3.2.8 on 2022-04-28 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0038_order_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_name',
        ),
    ]
