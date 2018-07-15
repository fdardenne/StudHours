from . import views
from django.urls import path

urlpatterns = [
    #path('<int:id>/', views.userid, name='idd'),
    path('', views.userboard, name='userboard'),
    path('profile/', views.profile, name="profile"),
    path('work/', views.work, name="work"),
    path('hours/', views.hour, name="hour"),
]