# Generated by Django 3.2.19 on 2023-06-09 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productinfo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='product_img',
            field=models.ImageField(blank=True, null=True, upload_to='product_img', verbose_name='商品图片'),
        ),
    ]