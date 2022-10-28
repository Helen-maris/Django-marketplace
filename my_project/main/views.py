from constance import config
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from main.models import Seller, Category, Tag, Ad, Picture, Subscription
from main.forms import UserForm, SellerForm, AdForm, ImageFormset
from main.tasks import send_mail_task


from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta



class IndexView(TemplateView):
    template_name = "main/index.html"
    extra_context = {'turn_on_block': config.MAINTENANCE_MODE}


class AdListView(ListView):
    model = Ad
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AdListView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

    def get_queryset(self):
        search_term = self.request.GET.get('tag', '')
        if search_term == '':
            return Ad.objects.all()
        else:
            return Ad.objects.filter(tag__name=search_term)


class AdDetailView(DetailView):
    model = Ad

    def get_context_data(self, **kwargs):

        picture = self.object.picture_set.all()
        context = super().get_context_data(**kwargs)
        context['picture'] = picture
        return context


class SellerUpdateView(UpdateView):

    model = Seller
    form_class = SellerForm
    template_name = 'main/seller_update.html'
    success_url = '/'

    def get_object(self):
        curr_seller = Seller.objects.get(user=self.request.user.id)
        return curr_seller

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        user_form = UserForm(data=self.request.POST, instance=self.request.user)
        user_form.save()
        return super().form_valid(form)


class AdCreateView(CreateView):

    model = Ad
    form_class = AdForm
    template_name = 'main/ad_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ImageFormset()
        return context

    def post(self, request):

        form = self.get_form()
        try:
            form.instance.seller = self.request.user.seller
        except ObjectDoesNotExist:
            form.instance.seller = Seller.objects.get_or_create(user=self.request.user)
        if form.is_valid():
            if form.instance.category.name == 'electronics':
                subscribers = Subscription.objects.first()
                emails = subscribers.user.all().values_list('email', flat=True)
                send_mail_task.delay(list(emails))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.FILES:
            new_ad = form.save()
            image_formset = ImageFormset(self.request.POST, self.request.FILES, instance=new_ad)
            if image_formset.is_valid():
                image_formset.save()
                return super().form_valid(form)
            else:
                return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('ad-detail', kwargs={'pk': self.object.pk})

      
class AdUpdateView(UpdateView):

    model = Ad
    form_class = AdForm
    template_name = 'main/ad_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ImageFormset()
        return context

    def post(self, request, pk):

        if self.request.FILES:
            instance = self.get_object()
            image_formset = ImageFormset(self.request.POST, self.request.FILES, instance=instance)
            if image_formset.is_valid():
                image_formset.save()
                return super().post(request)
            else:
                form = self.get_form()
                return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy('ad-detail', kwargs={'pk': self.object.pk})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Common group')
        instance.groups.add(group)


def weekly_mail():
    week_before = date.today() - timedelta(7)
    curr_week_ads = Ad.objects.filter(create_date__gte=week_before).values_list('name', flat=True)
    subscribers = Subscription.objects.first()
    emails = subscribers.user.all().values_list('email', flat=True)
    return curr_week_ads, emails
