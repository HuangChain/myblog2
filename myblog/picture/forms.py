# -*- coding: utf-8 -*-
from django import forms

from picture.models import Picture


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('image',)
