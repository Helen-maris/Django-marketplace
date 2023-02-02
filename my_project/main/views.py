from datetime import date, timedelta
import random

from constance import config
# from apscheduler.schedulers.background import BackgroundScheduler

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
# from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db.models.signals import post_save
from django.db.models.query import QuerySet
from django.dispatch import receiver
from django.shortcuts import render

from main.models import Seller, Tag, Ad, Subscription, SMSLog
from main.forms import UserForm, SellerForm, AdForm, ImageFormset, SMSLogForm
from main.tasks import send_mail_task, generate_code_task


def index(request):
    context = {'turn_on_block': config.MAINTENANCE_MODE}
    return render(request, "main/index.html", context)


# @method_decorator(cache_page(60 * 5), name='dispatch')
class AdListView(ListView):
    model = Ad
    template_name = 'ad_list.html'
    paginate_by = 10
    ordering = ['-create_date']

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

    def get_queryset(self) -> QuerySet:
        tag_name = self.request.GET.get('tag')
        queryset = super().get_queryset()
        if tag_name is None:
            return queryset
        else:
            return queryset.filter(tag__name=tag_name).order_by('pk')


@method_decorator(login_required(login_url='/accounts/login/'),
                  name='dispatch')
class MyAdsListView(ListView):

    model = Ad
    paginate_by = 10
    template_name = 'main/my_ads.html'

    def get_queryset(self) -> QuerySet:
        return Ad.objects.filter(seller__user__id=self.request.user.id)


# @method_decorator(cache_page(60 * 5), name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get_context_data(self, **kwargs) -> dict:
        picture = self.object.picture_set.all()
        context = super().get_context_data(**kwargs)
        context['picture'] = picture
        return context

    def get_object(self) -> object:
        obj = super().get_object()
        price_object = cache.get('price_object')
        if price_object is None:
            price_coef = round(random.uniform(0.8, 1.2), 1)
            obj.price = round(obj.price * price_coef)
            price_object = obj.price
            cache.set('price_object', price_object, timeout=60)
        obj.price = price_object
        return obj


@method_decorator(login_required(login_url='/accounts/login/'),
                  name='dispatch')
class SellerUpdateView(UpdateView):
    model = Seller
    form_class = SellerForm
    template_name = 'main/seller_update.html'
    success_url = '/'

    def get_object(self) -> object:
        user = self.request.user
        curr_seller, created = Seller.objects.get_or_create(user=user)
        return curr_seller

    def get_context_data(self, **kwargs) -> dict:
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        context['smslog_form'] = SMSLogForm()
        return context

    def post(self, request):
        self.object = self.get_object()
        form = self.get_form()
        # есть ли у пользователя сохраненный телефон
        if form.instance.phone:
            has_phone = True
        else:
            has_phone = False
        if form.is_valid():
            form.save()
            if has_phone and form.instance.phone:
                sms = SMSLog.objects.get(seller=self.object)
                smslog_form = SMSLogForm(self.request.POST, instance=sms)
                if smslog_form.is_valid():
                    user_code = smslog_form.instance.code
                    if sms.code == user_code:
                        smslog_form.instance.confirmed = True
                        smslog_form.save()
                        return self.form_valid(form)
                    else:
                        messages.error(request, "Неверный код!")
                        return HttpResponseRedirect(reverse('seller-update'))
            else:
                if form.instance.phone:
                    sms_code = random.randint(1000, 9999)
                    args = (sms_code, form.instance.phone)
                    generate_code_task.delay(args)
                    smslog_form = SMSLogForm(self.request.POST)
                    if smslog_form.is_valid():
                        user = self.request.user
                        curr_seller = Seller.objects.get(user=user)
                        smslog_form.instance.seller = curr_seller
                        smslog_form.instance.code = sms_code
                        smslog_form.save()
                    return HttpResponseRedirect(reverse('seller-update'))
                else:
                    return HttpResponseRedirect('/')
        return self.form_invalid(form)


@method_decorator(login_required(login_url='/accounts/login/'),
                  name='dispatch')
class AdCreateView(CreateView):

    model = Ad
    form_class = AdForm
    template_name = 'main/ad_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_formset'] = ImageFormset(
            self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.object or None
        )
        return context

    def post(self, request):
        form = self.get_form()
        form.instance.seller = self.request.user.seller
        if form.is_valid():
            """if form.instance.category.name == 'electronics':
                subscribers = Subscription.objects.first()
                emails = subscribers.user.all().values_list('email', flat=True)
                send_mail_task.delay(list(emails))"""
            self.object = form.save()
            context = self.get_context_data()
            image_formset = context['image_formset']
            if image_formset.is_valid():
                image_formset.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('ad-detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='/accounts/login/'),
                  name='dispatch')
class AdUpdateView(UpdateView):

    model = Ad
    form_class = AdForm
    template_name = 'main/ad_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        print("1", self.object.pk)
        context['image_formset'] = ImageFormset(
            self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.object
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            context = self.get_context_data()
            image_formset = context['image_formset']
            if image_formset.is_valid():
                image_formset.save()
            return self.form_valid(form)
        return form.invalid()

    def get_success_url(self):

        return reverse_lazy('ad-detail', kwargs={'pk': self.object.pk})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Common group')
        instance.groups.add(group)


def weekly_mail():
    week_before = date.today() - timedelta(7)
    curr_week_ads = Ad.objects.filter(
        create_date__gte=week_before).values_list('name', flat=True)
    subscribers = Subscription.objects.first()
    emails = subscribers.user.all().values_list('email', flat=True)
    return curr_week_ads, emails
