# Generated by Django 4.1.7 on 2023-04-18 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0052_rename_composition_product_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='pukar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=1000),
        ),
    ]