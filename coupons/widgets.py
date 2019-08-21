# -*- coding: utf-8 -*-
# filename: coupons/widgets.py
from django.forms.widgets import FileInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class NonClearableImageInput(FileInput):
    def render(self, name, value, attrs=None):
        template = '%(input)s'
        data = {'input': None, 'url': None}
        data['input'] = super(NonClearableImageInput, self).render(name, value, attrs)

        if hasattr(value, 'url'):
            data['url'] = conditional_escape(value.url)
            template = '%(input)s <img class="img-thumbnail" src="%(url)s">'

        return mark_safe(template % data)

