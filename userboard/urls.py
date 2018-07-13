from . import views
from django.urls import path

urlpatterns = [
    #path('<int:id>/', views.userid, name='idd'),
    path('', views.userboard, name='userboard'),
]