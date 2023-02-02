from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from .models import Seller, Category, Tag, Ad, Picture, Subscription

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }


class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'num_ads')


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Ad)
admin.site.register(Picture)
admin.site.register(Subscription)
