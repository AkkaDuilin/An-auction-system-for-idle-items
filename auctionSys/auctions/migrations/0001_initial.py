# Generated by Django 2.0.4 on 2023-06-01 10:10

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
            name='AuctionInfo',
            fields=[
                ('auction_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('auction_date', models.DateTimeField(auto_now=True)),
                ('auction_final_date', models.DateTimeField()),
                ('is_Active', models.BooleanField(default=True)),
                ('starting_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField()),
                ('current_bid', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('bid_count', models.IntegerField(default=0)),
                ('auction_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_part.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Bidder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_part.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='BidderList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidders', models.ManyToManyField(to='auctions.Bidder')),
            ],
        ),
        migrations.AddField(
            model_name='auctioninfo',
            name='bidder_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.BidderList'),
        ),
        migrations.AddField(
            model_name='auctioninfo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductInfo'),
        ),
        migrations.AddField(
            model_name='auctioninfo',
            name='winning_bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.Bidder'),
        ),
    ]
