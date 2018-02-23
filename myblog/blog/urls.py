from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from blog import views

urlpatterns = [
    url(r'^home/', views.HomeView.as_view(), name='home'),
    url(r'^articles/$', views.ArticleView.as_view(), name='articles'),
    url(r'^article_detail/(?P<id>\d+)$', views.DetailView.as_view(), name='detail'),
    url(r'^publish/$', views.PublishView.as_view(), name='publish'),
    url(r'^messages/', views.MessageView.as_view(), name='messages'),
    url(r'^article-likes/(?P<ids>\d+)/$', views.LikeView.as_view(), name='article_likes'),
    url(r'^edit/(?P<ids>\d+)/$', views.EditView.as_view(), name='edit'),
    url(r'^delete_article/(?P<ids>\d+)/$', views.DeleteView.as_view(), name='delete_article'),
]
