# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-17 11:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0005_auto_20190817_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='futurecoupon',
            old_name='futures_coupon_template_id',
            new_name='futures_coupon_template',
        ),
    ]
