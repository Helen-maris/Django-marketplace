from django.contrib.auth.models import User
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter

from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives


class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = User.objects.filter(email=sociallogin.user.email).first()
        if user and not sociallogin.is_existing:
            sociallogin.connect(request, user)
