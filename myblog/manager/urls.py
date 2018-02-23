from django.conf.urls import url

from manager import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^verify/', views.VerifyView.as_view(), name="verify"),
]
