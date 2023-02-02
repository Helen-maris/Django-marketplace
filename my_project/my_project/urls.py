from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from allauth.account.views import LoginView

from main.views import AdListView, MyAdsListView
from main.views import AdDetailView
from main.views import SellerUpdateView
from main.views import AdCreateView, AdUpdateView, index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ads/', AdListView.as_view(), name='ad-list'),
    path('my_ads/', MyAdsListView.as_view(), name='my-ads'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('accounts/seller/', SellerUpdateView.as_view(), name='seller-update'),
    path('ads/add/', AdCreateView.as_view(), name='ad-create'),
    path('ads/<int:pk>/edit/', AdUpdateView.as_view(), name='ad-update'),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
