# -*- coding: utf-8 -*-
# filename: coupons\urls.py

from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^my_coupons/$', views.my_coupon_list, name='my_coupons'),
                  url(r'^new_coupon/$', views.new_coupon, name='new_coupon'),
                  url(r'^edit_coupon/(?P<coupon_id>\d+)/$', views.edit_coupon, name='edit_coupon'),
                  url(r'^del_coupon/(?P<coupon_id>\d+)/$', views.del_coupon, name='del_coupon'),
                  url(r'^search_my_coupons/$', views.search_my_coupons, name='search_my_coupons'),
                  url(r'^search_market/$', views.search_market, name='search_market'),
                  url(r'^edit_merchant/$', views.edit_merchant, name='edit_merchant'),
                  url(r'^change_password/$', views.change_password, name='change_password'),
                  url(r'^change_password_done/$', views.change_password_done, name='change_password_done'),
                  url(r'^edit_user_data/$', views.edit_user_data, name='edit_user_data'),
                  url(r'^personal_coupon_template_list/$', views.personal_coupon_template_list,
                      name='personal_coupon_template_list'),
                  url(r'^new_personal_coupon_template/$', views.new_personal_coupon_template,
                      name='new_personal_coupon_template'),
                  url(r'^edit_personal_coupon_template/(?P<personal_coupon_template_id>\d+)/$',
                      views.edit_personal_coupon_template, name='edit_personal_coupon_template'),
                  url(r'^del_personal_coupon_template/(?P<personal_coupon_template_id>\d+)/$',
                      views.del_personal_coupon_template, name='del_personal_coupon_template'),
                  url(r'^search_personal_coupons_template/$', views.search_personal_coupons_template,
                      name='search_personal_coupons_template'),
                  url(r'^transfer_coupon/$', views.transfer_coupon,
                      name='transfer_coupon'),
                  url(r'^merchant_coupon_template_list/$', views.merchant_coupon_template_list,
                      name='merchant_coupon_template_list'),
                  url(r'^new_merchant_coupon_template/$', views.new_merchant_coupon_template,
                      name='new_merchant_coupon_template'),
                  url(r'^edit_merchant_coupon_template/(?P<merchant_coupon_template_id>\d+)/$',
                      views.edit_merchant_coupon_template, name='edit_merchant_coupon_template'),
                  url(r'^del_merchant_coupon_template/(?P<merchant_coupon_template_id>\d+)/$',
                      views.del_merchant_coupon_template, name='del_merchant_coupon_template'),
                  url(r'^search_merchant_coupons_template/$', views.search_merchant_coupons_template,
                      name='search_merchant_coupons_template'),
                  url(r'^merchant_release_coupon/$', views.merchant_release_coupon,
                      name='merchant_release_coupon'),
                  url(r'^merchant_release_coupon/$', views.merchant_release_coupon,
                      name='merchant_release_coupon'),
                  url(r'^use_coupon/$', views.use_coupon,
                      name='use_coupon'),
                  url(r'^manage_merchant_coupons/$', views.get_merchant_coupons,
                      name='manage_merchant_coupons'),
                  url(r'^delete_coupon_by_ids/$', views.delete_coupon_by_ids,
                      name='delete_coupon_by_ids'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
