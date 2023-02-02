from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField
from allauth.account.signals import user_signed_up


class BaseModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    itn = models.CharField(max_length=12, default=0)
    image = ImageField(default='world.png')
    phone = models.CharField(max_length=12, blank=True, null=True)

    @property
    def num_ads(self):
        return Ad.objects.filter(seller_id=self.pk).count()

    @receiver(user_signed_up)
    def after_user_signed_up(request, user, **kwargs):
        seller = Seller.objects.create(user=user)
        seller.save()

    def __str__(self):
        return self.user.username


class Category(BaseModel):
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Tag(BaseModel):

    def __str__(self):
        return self.name


class Ad(BaseModel):
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    edit_date = models.DateField(auto_now=True)
    tag = models.ManyToManyField(Tag)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        permissions = (
            ('create_ads', "Can create new ads"),
            ('view_ads', "Can view ads"),
        )

    def __str__(self):
        return self.name


class ArchiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category='archive')


class ArchiveAds(Ad):
    archive = ArchiveManager()

    class Meta:
        proxy = True


class Picture(models.Model):
    image = models.ImageField()
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)


class Subscription(models.Model):
    user = models.ManyToManyField(User)


class SMSLog(models.Model):

    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    code = models.CharField(max_length=4, blank=True, null=True)
    confirmed = models.BooleanField(blank=True, null=True)
    response = models.CharField(max_length=50)
