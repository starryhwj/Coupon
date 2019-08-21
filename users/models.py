# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    wechat_id = models.CharField(verbose_name='微信号', max_length=128, null=True, blank=True)
    phone = models.CharField(verbose_name='电话', max_length=128, null=True, blank=True)
    level = models.IntegerField(verbose_name='用户等级', null=True, blank=True)
    head_pic = models.ImageField(verbose_name='头像', upload_to='images/users/%Y/%m/%d/', null=True, blank=True)
    is_merchant = models.BooleanField(verbose_name='是否是商家', null=False, default=False)
    wallet_money = models.BooleanField(verbose_name='账户余额', null=False, default=False)

