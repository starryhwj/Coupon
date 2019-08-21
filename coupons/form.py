# -*- coding: utf-8 -*-
# filename: form.py

from django import forms
from models import Coupon, Merchant, PersonalCouponTemplate, MerchantCouponTemplate
from widgets import NonClearableImageInput
from users.models import User


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['no', 'password', 'pic', 'name', 'remark', 'begin_date', 'end_date', 'is_long_term', 'is_public',
                  'price']
        labels = {'no': u'编号', 'password': u'密码', 'pic': u'优惠券照片', 'name': u'名称', 'remark': u'备注',
                  'begin_date': u"起始日期", 'end_date': u'结束日期', 'is_long_term': u'是否长期有效',
                  'is_public': u'是否公开', 'price': u'价格'}
        widgets = {'no': forms.TextInput(), 'password': forms.TextInput(), 'name': forms.TextInput(),
                   'remark': forms.Textarea(attrs={'rows': 3}), 'pic': NonClearableImageInput}
        help_texts = {
            'pic': u'图片不能大于1M'
        }
        error_messages = {
            'no': {'required': u'编号不能为空',
                   'max_length': u'编号不能超过128位'},
            'password': {'required': u'密码不能为空',
                         'max_length': u'密码不能超过128位'},
            'pic': {'required': u'图片不能为空',
                    'invalid_image': u'请上传正确格式的图片！'},
            'name': {'required': u'名称不能为空',
                     'max_length': u'名称不能超过150位'},
            'remark': {'required': u'备注不能为空',
                       'max_length': u'备注不能超过128位'},
            'price': {'required': u'价格不能为空'},
        }

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        self.fields['begin_date'].required = False
        self.fields['end_date'].required = False


class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['name', 'head_pic', 'contact', 'remark']
        labels = {'name': u'店名', 'head_pic': u'店铺头像', 'contact': u'联系方式', 'remark': u'备注'}
        widgets = {'name': forms.TextInput(),  'head_pic': NonClearableImageInput, 'contact': forms.TextInput(),
                   'remark': forms.Textarea(attrs={'rows': 3})}
        help_texts = {
            'pic': u'图片不能大于1M'
        }
        error_messages = {
            'name': {'required': u'店名不能为空',
                     'max_length': u'店名不能超过128位'},
            'contact': {'required': u'联系方式不能为空',
                        'max_length': u'联系方式不能超过128位'},
            'head_pic': {'required': u'头像不能为空',
                         'invalid_image': u'请上传正确格式的头像！'},
            'remark': {'required': u'备注不能为空',
                       'max_length': u'备注不能超过128位'}
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'wechat_id', 'phone', 'head_pic']
        labels = {'email': u'电子邮件', 'wechat_id': u'微信号', 'phone': u'电话', 'head_pic': u'头像'}
        widgets = {'email': forms.TextInput(attrs={'type': 'email'}),  'wechat_id': forms.TextInput(),
                   'phone': forms.TextInput(attrs={'pattern': '(\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$'}),
                   'head_pic': NonClearableImageInput}
        help_texts = {
            'head_pic': u'图片不能大于1M'
        }
        error_messages = {
            'email': { 'max_length': u'电子邮件不能超过254位'},
            'wechat_id': {'max_length': u'微信号不能超过128位'},
            'head_pic': {'invalid_image': u'请上传正确格式的头像！'},
            'phone': {'invalid': u'电话号码格式不正确'}
        }


class PersonalCouponTemplateForm(forms.ModelForm):
    class Meta:
        model = PersonalCouponTemplate
        fields = ['pic', 'name', 'remark', 'begin_date', 'end_date', 'is_long_term', 'is_public',
                  'price']
        labels = {'pic': u'优惠券照片', 'name': u'名称', 'remark': u'备注',
                  'begin_date': u"起始日期", 'end_date': u'结束日期', 'is_long_term': u'是否长期有效',
                  'is_public': u'是否公开', 'price': u'价格'}
        widgets = {'name': forms.TextInput(),
                   'remark': forms.Textarea(attrs={'rows': 3}), 'pic': NonClearableImageInput}
        help_texts = {
            'pic': u'图片不能大于1M'
        }
        error_messages = {
            'pic': {'required': u'图片不能为空',
                    'invalid_image': u'请上传正确格式的图片！'},
            'name': {'required': u'名称不能为空',
                     'max_length': u'名称不能超过150位'},
            'remark': {'required': u'备注不能为空',
                       'max_length': u'备注不能超过128位'},
            'price': {'required': u'价格不能为空'},
        }


class MerchantCouponTemplateForm(forms.ModelForm):
    class Meta:
        model = MerchantCouponTemplate
        fields = ['pic', 'name', 'remark', 'begin_date', 'end_date', 'is_long_term', 'is_public',
                  'price']
        labels = {'pic': u'优惠券照片', 'name': u'名称', 'remark': u'备注',
                  'begin_date': u"起始日期", 'end_date': u'结束日期', 'is_long_term': u'是否长期有效',
                  'is_public': u'是否公开', 'price': u'价格'}
        widgets = {'name': forms.TextInput(),
                   'remark': forms.Textarea(attrs={'rows': 3}), 'pic': NonClearableImageInput}
        help_texts = {
            'pic': u'图片不能大于1M'
        }
        error_messages = {
            'pic': {'required': u'图片不能为空',
                    'invalid_image': u'请上传正确格式的图片！'},
            'name': {'required': u'名称不能为空',
                     'max_length': u'名称不能超过150位'},
            'remark': {'required': u'备注不能为空',
                       'max_length': u'备注不能超过128位'},
            'price': {'required': u'价格不能为空'},
        }


class MerchantReleaseCouponForm(forms.Form):
    coupons_template = forms.ModelChoiceField(queryset=None, empty_label="请选择模板", label="模板")
    target_name = forms.CharField(label="用户账号")
    count = forms.IntegerField(label="数量")

    def __init__(self, *args, **kwargs):
        merchant = kwargs.pop('merchant')
        super(MerchantReleaseCouponForm, self).__init__(*args, **kwargs)
        if merchant:
            self.fields['coupons_template'].queryset = MerchantCouponTemplate.objects.filter(merchant=merchant,
                                                                                             is_active=True)


class UseCouponForm(forms.Form):
    no = forms.CharField(label="编号")
    password = forms.CharField(label="密码")

