# -*- coding: utf-8 -*-
# filename: users/form.py

from django.contrib.auth.forms import UserCreationForm
from models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

