# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Coupon, CouponOperation

admin.site.register(Coupon)
admin.site.register(CouponOperation)

