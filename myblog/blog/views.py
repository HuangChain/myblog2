# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from blog.models import Blog, Message
from manager.models import UserInfo
from blog.forms import BlogForm, MessageForm

# Create your views here.


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class CsrfExemptMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CsrfExemptMixin, cls).as_view(**initkwargs)
        return csrf_exempt(view)


class HomeView(View):

    def get(self, request):
        blogs = Blog.objects.all()[:3]
        userinfo = UserInfo.objects.get(user_id=1)
        return render(request, 'home.html', {
            'blogs': blogs,
            'userinfo': userinfo
        })


class ArticleView(View):

    def get(self, request):
        articles = Blog.objects.all()
        total_articles = articles.count()
        paginator = Paginator(articles, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        articles = Blog.objects.all().order_by("-likes")[:5]
        return render(request, 'articles.html', {
            'contacts': contacts,
            'articles': articles,
            'total_articles': total_articles
        })


class DetailView(View):

    def get(self, request, id):
        article = Blog.objects.get(id=id)
        likes = range(article.likes)
        if cache.has_key("article{}".format(article.id)):
            total_views = cache.incr("article{}".format(article.id), 1)
        else:
            cache.set("article{}".format(article.id), 0)
        total_views = cache.get("article{}".format(article.id))
        return render(request, 'detail.html', {
            'article': article,
            'likes': likes,
            'total_views': total_views
        })


class PublishView(LoginRequiredMixin, CsrfExemptMixin,  View):

    def get(self, request):
        article_form = BlogForm()
        return render(request, 'publish.html', {'article_form': article_form})

    def post(self, request):
        article_form = BlogForm(request.POST)
        if article_form.is_valid():
            cd = article_form.cleaned_data
            Blog.objects.create(title=cd['title'], body=cd['body'])
            return HttpResponse('1')
        else:
            return JsonResponse(article_form.errors)
        return JsonResponse(article_form.errors)


class LikeView(CsrfExemptMixin, View):

    def post(self, request, ids):
        article = Blog.objects.get(id=ids)
        article.likes += 1
        article.save()
        return HttpResponse('1')


class MessageView(CsrfExemptMixin, View):

    def get(self, request):
        message_form = MessageForm()
        messages = Message.objects.filter(status=1).order_by("-created")
        return render(
            request,
            'messages.html',
            context={
                'messages': messages,
                'message_form': message_form
            }
        )

    def post(self, request):
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            cd = message_form.cleaned_data
            Message.objects.create(message=cd['message'])
            return HttpResponse('1')
        else:
            return JsonResponse(message_form.errors)
        return JsonResponse(message_form.errors)


class EditView(LoginRequiredMixin, CsrfExemptMixin, View):

    def get(self, request, ids):
        article = Blog.objects.get(id=ids)
        article_form = BlogForm(initial={'title': article.title, 'body': article.body})
        return render(request, 'edit.html', {'article_form': article_form, 'article':article})

    def post(self, request, ids):
        article_form = BlogForm(request.POST)
        if article_form.is_valid():
            cd = article_form.cleaned_data
            Blog.objects.filter(id=ids).update(title=cd['title'], body=cd['body'])
            return HttpResponse('1')
        else:
            return JsonResponse(article_form.errors)
        return JsonResponse(article_form.errors)


class DeleteView(LoginRequiredMixin, CsrfExemptMixin, View):

    def post(self, request, ids):
        Blog.objects.get(id=ids).delete()
        return HttpResponse('1')

