from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('<int:id>/', views.userid, name='idd'),
    path('', views.userboard, name='userboard'),
    path('profile/', views.profile, name="profile"),
    path('work/', views.work, name="work"),
    path('hours/', views.hour, name="hour"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
