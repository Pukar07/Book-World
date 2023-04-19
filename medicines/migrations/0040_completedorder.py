# Generated by Django 3.2.8 on 2022-05-08 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0039_remove_order_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='completedOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicines.order')),
            ],
        ),
    ]
