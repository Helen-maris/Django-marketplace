"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from allauth.account.views import LoginView

from main.views import AdListView
from main.views import AdDetailView
from main.views import SellerUpdateView
from main.views import AdCreateView, AdUpdateView, IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ads/', AdListView.as_view(), name='ad-list'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('accounts/seller/', login_required(SellerUpdateView.as_view(), redirect_field_name=None), name='seller-update'),
    path('ads/add/', login_required(AdCreateView.as_view(), redirect_field_name=None), name='ad-create'),
    path('ads/<int:pk>/edit/', login_required(AdUpdateView.as_view(), redirect_field_name=None), name='ad-update'),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
