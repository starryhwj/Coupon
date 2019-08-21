# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from users.models import User


class Merchant(models.Model):
    owner = models.ForeignKey(User, verbose_name='掌柜', on_delete=models.CASCADE)
    name = models.TextField(verbose_name='名称', max_length=150, null=False)
    is_active = models.BooleanField(verbose_name='是否激活', null=False, default=True)
    date_join = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    level = models.IntegerField(verbose_name='店铺等级', null=True, blank=True)
    head_pic = models.ImageField(verbose_name='头像', upload_to='images/merchants/%Y/%m/%d/', null=True, blank=True)
    remark = models.TextField(verbose_name='备注', max_length=254, null=False)
    contact = models.TextField(verbose_name='联系方式', max_length=254, null=False)


class Coupon(models.Model):
    owner = models.ForeignKey(User, verbose_name='拥有者', on_delete=models.CASCADE, related_name='coupon_owner')
    no = models.TextField(verbose_name='编号', max_length=128, null=False)
    password = models.TextField(verbose_name='密码', max_length=128, null=False)
    pic = models.ImageField(verbose_name='图片', upload_to='images/coupons/%Y/%m/%d/')
    name = models.TextField(verbose_name='名称', max_length=150, null=False)
    remark = models.TextField(verbose_name='备注', max_length=254, null=False)
    begin_date = models.DateTimeField(verbose_name='起始日期', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='结束日期', null=True, blank=True)
    is_long_term = models.BooleanField(verbose_name='是否长期有效', null=False)
    is_public = models.BooleanField(verbose_name='是否公开', null=False, default=True)
    price = models.DecimalField(verbose_name='售价', max_digits=18, decimal_places=2)
    type = models.IntegerField(verbose_name='类型')
    is_used = models.BooleanField(verbose_name='是否已使用')
    create_user = models.ForeignKey(User, verbose_name='创建用户', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='create_user')
    merchant = models.ForeignKey(Merchant, verbose_name='创建店铺', on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='是否激活', null=False, default=True)
    is_lock = models.BooleanField(verbose_name='是否锁定', null=False, default=False)


class CouponOperation(models.Model):
    coupon = models.ForeignKey(Coupon, verbose_name='优惠券', on_delete=models.CASCADE)
    operation_type = models.IntegerField(verbose_name='操作类型', null=False)
    operation_date = models.DateTimeField(verbose_name='操作日期', auto_now_add=True)
    operation_user = models.ForeignKey(User, verbose_name='操作人', on_delete=models.CASCADE,
                                       related_name='coupon_operation_operation_user')
    old_owner = models.ForeignKey(User, verbose_name='前拥有者', on_delete=models.CASCADE,
                                  related_name='coupon_operation_old_owner')
    new_owner = models.ForeignKey(User, verbose_name='新拥有者', on_delete=models.CASCADE,
                                  related_name='coupon_operation_new_owner')


class MerchantCouponTemplate(models.Model):
    merchant = models.ForeignKey(Merchant, verbose_name='所属店铺', on_delete=models.CASCADE)
    pic = models.ImageField(verbose_name='图片', upload_to='images/merchant-coupon-template/%Y/%m/%d/')
    name = models.TextField(verbose_name='名称', max_length=150, null=False)
    remark = models.TextField(verbose_name='备注', max_length=254, null=False)
    begin_date = models.DateTimeField(verbose_name='起始日期', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='结束日期', null=True, blank=True)
    is_long_term = models.BooleanField(verbose_name='是否长期有效', null=False)
    is_public = models.BooleanField(verbose_name='是否公开', null=False, default=True)
    price = models.DecimalField(verbose_name='售价', max_digits=18, decimal_places=2)
    is_active = models.BooleanField(verbose_name='是否激活', null=False, default=True)
    create_date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)

    def __unicode__(self):
        return self.name


class PersonalCouponTemplate(models.Model):
    owner = models.ForeignKey(User, verbose_name='拥有者', on_delete=models.CASCADE)
    pic = models.ImageField(verbose_name='图片', upload_to='images/personal-coupon-template/%Y/%m/%d/')
    name = models.TextField(verbose_name='名称', max_length=150, null=False)
    remark = models.TextField(verbose_name='备注', max_length=254, null=False)
    begin_date = models.DateTimeField(verbose_name='起始日期', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='结束日期', null=True, blank=True)
    is_long_term = models.BooleanField(verbose_name='是否长期有效', null=False)
    is_public = models.BooleanField(verbose_name='是否公开', null=False, default=True)
    price = models.DecimalField(verbose_name='售价', max_digits=18, decimal_places=2)
    is_active = models.BooleanField(verbose_name='是否激活', null=False, default=True)
    create_date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)


class WalletMoneyRecord(models.Model):
    owner = models.ForeignKey(User, verbose_name='持有人', on_delete=models.CASCADE,
                              related_name='wallet_money_record_owner')
    type = models.IntegerField(verbose_name='类型')
    original = models.DecimalField(verbose_name='更改前余额', max_digits=18, decimal_places=2)
    change = models.DecimalField(verbose_name='更改金额', max_digits=18, decimal_places=2)
    change_date = models.DateTimeField(verbose_name='更改日期', null=True, blank=True)
    change_user = models.ForeignKey(User, verbose_name='更改人', on_delete=models.CASCADE, related_name='change_user')


class FutureCouponTemplate(models.Model):
    merchant = models.ForeignKey(Merchant, verbose_name='所属店铺', on_delete=models.CASCADE)
    discount = models.DecimalField(verbose_name='折扣', max_digits=18, decimal_places=1)
    minimum_quote = models.DecimalField(verbose_name='最低额度', max_digits=18, decimal_places=2)
    issue_price = models.DecimalField(verbose_name='发行价', max_digits=18, decimal_places=2)
    price = models.DecimalField(verbose_name='售价', max_digits=18, decimal_places=2)
    bing_data = models.TextField(verbose_name='绑定数据', max_length=150, null=False)
    now_quote = models.DecimalField(verbose_name='当前额度', max_digits=18, decimal_places=2)
    begin_count_down_date = models.DateTimeField(verbose_name='期货状态起始日期')
    end_count_down_date = models.DateTimeField(verbose_name='期货状态结束日期')
    count = models.IntegerField(verbose_name='数量')
    pic = models.ImageField(verbose_name='图片', upload_to='images/future-coupon-template/%Y/%m/%d/')
    name = models.TextField(verbose_name='名称', max_length=150, null=False)
    remark = models.TextField(verbose_name='备注', max_length=254, null=False)
    begin_date = models.DateTimeField(verbose_name='起始日期', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='结束日期', null=True, blank=True)
    is_long_term = models.BooleanField(verbose_name='是否长期有效', null=False)
    is_active = models.BooleanField(verbose_name='是否激活', null=False, default=True)
    create_date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)


class FutureCoupon(models.Model):
    futures_coupon_template = models.ForeignKey(Merchant, verbose_name='所属模板', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name='持有人', on_delete=models.CASCADE, related_name='future_coupon_owner')
    price = models.DecimalField(verbose_name='售价', max_digits=18, decimal_places=2)
    is_public = models.BooleanField(verbose_name='是否公开', null=False, default=True)
    create_date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    is_lock = models.BooleanField(verbose_name='是否锁定', null=False, default=False)


class FutureCouponOrder(models.Model):
    seller = models.ForeignKey(User, verbose_name='卖家', on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, verbose_name='买家', on_delete=models.CASCADE, related_name='buyer')
    total_price = models.DecimalField(verbose_name='总售价', max_digits=18, decimal_places=2)
    trade_date = models.DateTimeField(verbose_name='交易日期', auto_now_add=True)
    status = models.IntegerField(verbose_name='交易状态')


class FutureCouponOrderDetail(models.Model):
    future_coupon_order = models.ForeignKey(FutureCouponOrder, verbose_name='所属订单', on_delete=models.CASCADE)
    future_coupon = models.ForeignKey(FutureCoupon, verbose_name='期货优惠券', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='售价', max_digits=18, decimal_places=2)


class FutureCouponOperation(models.Model):
    future_coupon = models.ForeignKey(FutureCoupon, verbose_name='优惠券', on_delete=models.CASCADE)
    operation_type = models.IntegerField(verbose_name='操作类型', null=False)
    operation_date = models.DateTimeField(verbose_name='操作日期', auto_now_add=True)
    operation_user = models.ForeignKey(User, verbose_name='操作人', on_delete=models.CASCADE,
                                       related_name='future_coupon_operation_operation_user')
    old_owner = models.ForeignKey(User, verbose_name='前拥有者', on_delete=models.CASCADE,
                                  related_name='future_coupon_operation_old_owner')
    new_owner = models.ForeignKey(User, verbose_name='新拥有者', on_delete=models.CASCADE,
                                  related_name='future_coupon_operation_new_owner')

