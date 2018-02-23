from django.conf.urls import url
from django.views.generic.list import ListView
from picture import views
from picture.models import Picture

picture = {
    'queryset': Picture.objects.all()
}

urlpatterns = [
    url(r'^', views.PictureListView.as_view(), name='pictures'),
    url(r'^create_picture', views.PictureCreateView.as_view(), name='create_picture'),

]
