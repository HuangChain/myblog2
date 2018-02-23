# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse_lazy

from picture.models import Picture
from picture.forms import PictureForm

# Create your views here.


class PictureListView(ListView):
    template_name = 'pictures.html'
    # context_object_name = 'pictures'
    model = Picture

    # def get_queryset(self):
    #     pictures = Picture.objects.all()
    #     return pictures


class PictureCreateView(CreateView):
    template_name = 'picture/pictures.html'
    form_class = PictureForm
    success_url = reverse_lazy('picture:pictures')


# class PictureView1(View):
#
#     def get(self, request):
#         pictures = Picture.objects.all()
#         return render(request, 'pictures.html', {'pictures': pictures})
#
#     def post(self, request):
#         picture_form = PictureForm(request.POST, request.FILES)
#         pictures = Picture.objects.all()
#         if picture_form.is_valid():
#             picture_form.save()
#             return render(request, 'pictures.html', {
#                 'pictures': pictures,
#                 'msg': u'上传成功'
#             })
#         else:
#             return render(request, 'pictures.html', {
#                 'pictures': pictures,
#                 'msg': u'请选择图片'
#             })
#         return render(request, 'pictures.html', {'pictures': pictures})
#
