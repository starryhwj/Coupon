# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-09 11:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupons', '0002_auto_20190802_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='images/coupons/%Y/%m/%d/', verbose_name='\u56fe\u7247')),
                ('name', models.TextField(max_length=150, verbose_name='\u540d\u79f0')),
                ('remark', models.TextField(max_length=254, verbose_name='\u5907\u6ce8')),
                ('begin_date', models.DateTimeField(blank=True, null=True, verbose_name='\u8d77\u59cb\u65e5\u671f')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='\u7ed3\u675f\u65e5\u671f')),
                ('is_long_term', models.BooleanField(verbose_name='\u662f\u5426\u957f\u671f\u6709\u6548')),
                ('is_public', models.BooleanField(default=True, verbose_name='\u662f\u5426\u516c\u5f00')),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='\u4ef7\u683c')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6fc0\u6d3b')),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=150, verbose_name='\u540d\u79f0')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6fc0\u6d3b')),
                ('date_join', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f')),
                ('level', models.IntegerField(blank=True, null=True, verbose_name='\u5e97\u94fa\u7b49\u7ea7')),
                ('head_pic', models.ImageField(blank=True, null=True, upload_to='images/users/%Y/%m/%d/', verbose_name='\u5934\u50cf')),
                ('remark', models.TextField(max_length=254, verbose_name='\u5907\u6ce8')),
                ('contact', models.TextField(max_length=254, verbose_name='\u8054\u7cfb\u65b9\u5f0f')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u638c\u67dc')),
            ],
        ),
        migrations.AddField(
            model_name='coupon',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65e5\u671f'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='create_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_id', to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u7528\u6237'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u6fc0\u6d3b'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='begin_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='\u8d77\u59cb\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='\u7ed3\u675f\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='is_public',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u516c\u5f00'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='\u62e5\u6709\u8005'),
        ),
        migrations.AlterField(
            model_name='couponoperation',
            name='operation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u64cd\u4f5c\u65e5\u671f'),
        ),
        migrations.AddField(
            model_name='coupontemplate',
            name='merchant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coupons.Merchant', verbose_name='\u6240\u5c5e\u5e97\u94fa'),
        ),
        migrations.AddField(
            model_name='coupontemplate',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u62e5\u6709\u8005'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='merchant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coupons.Merchant', verbose_name='\u521b\u5efa\u5e97\u94fa'),
        ),
    ]
