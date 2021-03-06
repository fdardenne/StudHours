"""StudentHours URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userboard import views
from django.conf import settings
from django.conf.urls.static import static


handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('adminManagement/', admin.site.urls),
    path('viewboard/', include('userboard.urls')),
    path('accounts/signup/', views.signup, name="signup"),
    path('accounts/', include('django.contrib.auth.urls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
