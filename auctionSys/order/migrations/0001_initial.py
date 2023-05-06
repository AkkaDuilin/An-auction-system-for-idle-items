# Generated by Django 2.0.4 on 2023-05-05 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('user_part', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('order_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('is_Pay', models.BooleanField(default=False)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('address', models.CharField(max_length=140)),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_part.Userinfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.OrderInfo'),
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductInfo'),
        ),
    ]