# -*- coding: utf-8 -*-
# -*- filename: users/views.py

from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from form import CustomUserCreationForm


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


def register(request):
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('coupons:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
