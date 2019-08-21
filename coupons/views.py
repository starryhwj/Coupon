# -*- coding: utf-8 -*-
# -*- filename: coupons\views.py
from __future__ import unicode_literals
from django.shortcuts import render
from models import Coupon, Merchant, PersonalCouponTemplate, MerchantCouponTemplate
from django.core.paginator import Paginator
from form import CouponForm, MerchantForm, UserForm, PersonalCouponTemplateForm, MerchantCouponTemplateForm, \
    MerchantReleaseCouponForm, UseCouponForm
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, authenticate
from users.models import User
import random


@login_required
def index(request):
    coupons = Coupon.objects.filter(~Q(owner=request.user), is_active=True, is_public=True).order_by('-create_date')
    data, return_coupon_list = get_page_data(coupons, request, 8)
    return render(request, 'coupons/index.html', context={
        'return_coupon_list': return_coupon_list, 'data': data
    })


@login_required
def my_coupon_list(request):
    coupon_template_list = PersonalCouponTemplate.objects.filter(owner=request.user)
    coupons = Coupon.objects.filter(owner=request.user, is_active=True)
    data, return_coupon_list = get_page_data(coupons, request, 8)
    return render(request, 'coupons/coupon_list.html', context={
        'return_coupon_list': return_coupon_list, 'data': data, 'coupon_template_list': coupon_template_list
    })


@login_required
def new_coupon(request):
    if request.method != 'POST':
        template_id = request.GET.get('template')
        if template_id == u'-1':  # 空白模板
            form = CouponForm()
        else:
            template = PersonalCouponTemplate.objects.get(id=template_id)
            data = {
                'name': template.name,
                'remark': template.remark,
                'is_long_term': template.is_long_term,
                'is_public': template.is_public,
                'price': template.price,
                'begin_date': template.begin_date,
                'end_date': template.end_date,
                'pic': template.pic
            }
            form = CouponForm(initial=data)
    else:
        template_id = request.POST.get('template_id')
        if len(request.FILES) == 0 and template_id != u'-1':
            template = PersonalCouponTemplate.objects.get(id=template_id)
            request.FILES['pic'] = template.pic
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            coupon = form.save(commit=False)
            coupon.owner = request.user
            coupon.create_user = request.user
            coupon.is_used = False
            coupon.type = 1
            coupon.save()
            return HttpResponseRedirect(reverse('coupons:my_coupons'))
        else:
            context = {'form': form, 'error': form.errors, 'template_id': template_id}
            return render(request, 'coupons/new_coupon.html', context)

    context = {'form': form, 'template_id': template_id}
    return render(request, 'coupons/new_coupon.html', context)


@login_required
def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    if coupon.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = CouponForm(instance=coupon)
    else:
        form = CouponForm(instance=coupon, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('coupons:my_coupons'))
        else:
            context = {'form': form, 'error': form.errors}
            return render(request, 'coupons/edit_coupon.html', context)

    context = {'form': form, 'coupon': coupon}
    return render(request, 'coupons/edit_coupon.html', context)


@login_required
def del_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    if coupon.owner != request.user:
        raise Http404
    coupon.is_active = False
    coupon.save()
    return HttpResponseRedirect(reverse('coupons:my_coupons'))


@login_required
def search_my_coupons(request):
    coupon_template_list = PersonalCouponTemplate.objects.filter(owner=request.user)
    key = request.GET.get('key')
    if key == "":
        return HttpResponseRedirect(reverse('coupons:my_coupons'))
    else:
        coupons = Coupon.objects.filter(owner=request.user, no__contains=key, is_active=True)
    data, return_coupon_list = get_page_data(coupons, request, 8)
    return render(request, 'coupons/coupon_list.html', context={
        'return_coupon_list': return_coupon_list, 'data': data, 'coupon_template_list': coupon_template_list
    })


def search_market(request):
    select = request.GET.get('search-select')
    if select == "优惠券":
        return search_market_coupons(request)
    else:
        return search_market_merchant(request)


def search_market_coupons(request):
    key = request.GET.get('key')
    if key == "":
        return HttpResponseRedirect(reverse('coupons:index'))
    else:
        coupons = Coupon.objects.filter(~Q(owner=request.user), no__contains=key, is_active=True, is_public=True) \
            .order_by('-create_date')
        data, return_coupon_list = get_page_data(coupons, request, 8)
        return render(request, 'coupons/index.html', context={
            'return_coupon_list': return_coupon_list, 'data': data
        })


def search_market_merchant(request):
    key = request.GET.get('key')

    if key == "":
        merchants = Merchant.objects.filter(~Q(owner=request.user), is_active=True).order_by('-date_join')
    else:
        merchants = Merchant.objects.filter(~Q(owner=request.user), name__contains=key, is_active=True) \
            .order_by('-date_join')

    data, return_merchant_list = get_page_data(merchants, request, 8)
    return render(request, 'coupons/index.html', context={
        'return_merchant_list': return_merchant_list, 'data': data, 'select': 'selected'
    })


def edit_merchant(request):
    merchant = Merchant.objects.get(owner=request.user)
    if request.method != 'POST':
        form = MerchantForm(instance=merchant)
    else:
        form = MerchantForm(instance=merchant, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('coupons:edit_merchant'))
        else:
            context = {'form': form, 'error': form.errors}
            return render(request, 'coupons/edit_merchant.html', context)

    context = {'form': form, 'merchant': merchant}
    return render(request, 'coupons/edit_merchant.html', context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            authenticated_user = authenticate(username=request.user.username, password=request.POST['new_password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('coupons:change_password_done'))
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form': form,
    }
    return render(request, 'coupons/change_password.html', context)


@login_required
def change_password_done(request):
    return render(request, 'coupons/change_password_done.html')


@login_required
def edit_user_data(request):
    user = request.user
    if request.method != 'POST':
        form = UserForm(instance=user)
    else:
        form = UserForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('coupons:edit_user_data'))
        else:
            context = {'form': form, 'error': form.errors}
            return render(request, 'coupons/edit_user_data.html', context)

    context = {'form': form}
    return render(request, 'coupons/edit_user_data.html', context)


@login_required
def personal_coupon_template_list(request):
    coupon_templates = PersonalCouponTemplate.objects.filter(owner=request.user, is_active=True).order_by('-create_date')
    data, return_coupon_template_list = get_page_data(coupon_templates, request, 8)
    return render(request, 'coupons/personal_coupon_template_list.html', context={
        'return_coupon_template_list': return_coupon_template_list, 'data': data
    })


@login_required
def new_personal_coupon_template(request):
    if request.method != 'POST':
        form = PersonalCouponTemplateForm()
    else:
        form = PersonalCouponTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            coupon_template = form.save(commit=False)
            coupon_template.owner = request.user
            coupon_template.save()
            return HttpResponseRedirect(reverse('coupons:personal_coupon_template_list'))
        else:
            context = {'form': form, 'error': form.errors}
            return render(request, 'coupons/new_personal_coupon_template.html', context)

    context = {'form': form}
    return render(request, 'coupons/new_personal_coupon_template.html', context)


@login_required
def edit_personal_coupon_template(request, personal_coupon_template_id):
    coupon_template = PersonalCouponTemplate.objects.get(id=personal_coupon_template_id)
    if coupon_template.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = PersonalCouponTemplateForm(instance=coupon_template)
    else:
        form = PersonalCouponTemplateForm(instance=coupon_template, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('coupons:personal_coupon_template_list'))
        else:
            context = {'form': form, 'error': form.errors}
            return render(request, 'coupons/edit_personal_coupon_template.html', context)

    context = {'form': form, 'coupon_template': coupon_template}
    return render(request, 'coupons/edit_personal_coupon_template.html', context)


@login_required
def del_personal_coupon_template(request, personal_coupon_template_id):
    coupon_template = PersonalCouponTemplate.objects.get(id=personal_coupon_template_id)
    if coupon_template.owner != request.user:
        raise Http404
    coupon_template.is_active = False
    coupon_template.save()
    return HttpResponseRedirect(reverse('coupons:personal_coupon_template_list'))


@login_required
def search_personal_coupons_template(request):
    key = request.GET.get('key')
    if key == "":
        return HttpResponseRedirect(reverse('coupons:personal_coupon_template_list'))
    else:
        coupons_template = PersonalCouponTemplate.objects.filter(owner=request.user, name__contains=key,
                                                                 is_active=True).order_by('-create_date')
    data, return_coupon_template_list = get_page_data(coupons_template, request, 8)
    return render(request, 'coupons/personal_coupon_template_list.html', context={
        'return_coupon_template_list': return_coupon_template_list, 'data': data
    })


def transfer_coupon(request):
    target_name = request.POST.get('target_name')
    coupon_id = request.POST.get('coupon_id')
    target_user = User.objects.get(username=target_name, is_active=True)
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.owner = target_user
    coupon.password = random.randint(0, 100)
    coupon.save()
    return HttpResponseRedirect(reverse('coupons:my_coupons'))


@login_required
def merchant_coupon_template_list(request):
    merchant = Merchant.objects.get(owner=request.user)
    coupon_templates = MerchantCouponTemplate.objects.filter(merchant=merchant, is_active=True).order_by('-create_date')
    data, return_coupon_template_list = get_page_data(coupon_templates, request, 8)
    return render(request, 'coupons/merchant_coupon_template_list.html', context={
        'return_coupon_template_list': return_coupon_template_list, 'data': data
    })


@login_required
def new_merchant_coupon_template(request):
    if request.method != 'POST':
        form = MerchantCouponTemplateForm()
    else:
        form = MerchantCouponTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            coupon_template = form.save(commit=False)
            merchant = Merchant.objects.get(owner=request.user)
            coupon_template.merchant = merchant
            coupon_template.save()
            return HttpResponseRedirect(reverse('coupons:merchant_coupon_template_list'))
        else:
            context = {'form': form, 'error': form.errors}
            return render(request, 'coupons/new_merchant_coupon_template.html', context)

    context = {'form': form}
    return render(request, 'coupons/new_merchant_coupon_template.html', context)


@login_required
def edit_merchant_coupon_template(request, merchant_coupon_template_id):
    coupon_template = MerchantCouponTemplate.objects.get(id=merchant_coupon_template_id)
    merchant = Merchant.objects.get(owner=request.user)
    if coupon_template.merchant != merchant:
        raise Http404
    if request.method != 'POST':
        form = MerchantCouponTemplateForm(instance=coupon_template)
    else:
        form = MerchantCouponTemplateForm(instance=coupon_template, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('coupons:merchant_coupon_template_list'))
        else:
            context = {'form': form, 'error': form.errors}
            return render(request, 'coupons/edit_merchant_coupon_template.html', context)

    context = {'form': form, 'coupon_template': coupon_template}
    return render(request, 'coupons/edit_merchant_coupon_template.html', context)


@login_required
def del_merchant_coupon_template(request, merchant_coupon_template_id):
    coupon_template = MerchantCouponTemplate.objects.get(id=merchant_coupon_template_id)
    merchant = Merchant.objects.get(owner=request.user)
    if coupon_template.merchant != merchant:
        raise Http404
    coupon_template.is_active = False
    coupon_template.save()
    return HttpResponseRedirect(reverse('coupons:personal_coupon_template_list'))


@login_required
def search_merchant_coupons_template(request):
    key = request.GET.get('key')
    if key == "":
        return HttpResponseRedirect(reverse('coupons:merchant_coupon_template_list'))
    else:
        merchant = Merchant.objects.get(owner=request.user)
        coupons_template = MerchantCouponTemplate.objects.filter(merchant=merchant, name__contains=key,
                                                                 is_active=True).order_by('-create_date')
    data, return_coupon_template_list = get_page_data(coupons_template, request, 8)
    return render(request, 'coupons/merchant_coupon_template_list.html', context={
        'return_coupon_template_list': return_coupon_template_list, 'data': data
    })


@login_required
def merchant_release_coupon(request):
    merchant = Merchant.objects.get(owner=request.user)
    if request.method != 'POST':
        form = MerchantReleaseCouponForm(merchant=merchant)
    else:
        form = MerchantReleaseCouponForm(merchant=merchant)
        target_name = request.POST.get('target_name')
        count = request.POST.get('count')
        coupons_template_id = request.POST.get('coupons_template')
        coupons_template = MerchantCouponTemplate.objects.get(id=coupons_template_id)
        target_user = User.objects.get(username=target_name, is_active=True)
        for i in range(0, int(count)):
            no = random.randint(0, 100)
            password = random.randint(0, 100)
            coupon = Coupon()
            coupon.no = no
            coupon.password = password
            coupon.pic = coupons_template.pic
            coupon.name = coupons_template.name
            coupon.remark = coupons_template.remark
            coupon.begin_date = coupons_template.begin_date
            coupon.end_date = coupons_template.end_date
            coupon.is_long_term = coupons_template.is_long_term
            coupon.is_public = coupons_template.is_public
            coupon.price = coupons_template.price
            coupon.owner = target_user
            coupon.create_user = request.user
            coupon.is_used = False
            coupon.type = 1
            coupon.save()
    context = {'form': form}
    return render(request, 'coupons/merchant_release_coupon.html', context)


@login_required
def use_coupon(request):
    if request.method != 'POST':
        form = UseCouponForm()
    else:
        form = UseCouponForm()
        no = request.POST.get('no')
        password = request.POST.get('password')
        coupons = Coupon.objects.filter(no=no, password=password)
        if coupons and len(coupons) > 0:
            coupon = coupons[0]
            coupon.is_used = True
            coupon.save()
    context = {'form': form}
    return render(request, 'coupons/use_coupon.html', context)


@login_required
def get_merchant_coupons(request):
    merchant = Merchant.objects.get(owner=request.user)
    key = request.GET.get('key', '')
    if key == "":
        merchant_coupon = Coupon.objects.filter(create_user=merchant.owner).order_by('-create_date')
    else:
        merchant_coupon = Coupon.objects.filter(create_user=merchant.owner, name__contains=key).order_by('-create_date')
    data, return_merchant_coupon_list = get_page_data(merchant_coupon, request, 10)
    context = {'return_merchant_coupon_list': return_merchant_coupon_list, 'data': data, 'key': key}
    return render(request, 'coupons/manage_merchant_coupons.html', context)


@login_required
def delete_coupon_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids.split(',')
    if len(ids) > 0:
        Coupon.objects.filter(id__in=id_list).update(is_active=False)
    return HttpResponse()


def get_page_data(objects, request, n):
    p = Paginator(objects, n)  # 分页，n个一页
    if p.num_pages <= 1:  # 如果不足一页
        return_list = objects  # 直接返回所有
        key = request.GET.get('key', "")  # 获取查询框关键字
        data = {
            'key': key,
            'has_value': False
        }  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取请求的页码，默认为第一页
        key = request.GET.get('key', "")  # 获取查询框关键字
        return_list = p.page(page)  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False  # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = list(p.page_range)
        if page == 1:  # 如果请求第1页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  # 如果请求最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {  # 将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
            'key': key,
            'has_value': True
        }
    return data, return_list
