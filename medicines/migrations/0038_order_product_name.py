# Generated by Django 3.2.8 on 2022-04-28 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0037_auto_20220428_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicines.product'),
        ),
    ]
