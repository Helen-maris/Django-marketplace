from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from main.models import Seller, Ad, Picture, SMSLog


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class SellerForm(ModelForm):

    def clean_itn(self):
        inn = self.cleaned_data['itn']

        if len(inn) not in (10, 12):
            raise ValidationError("Неверный ИНН")

        def inn_csum(inn):
            k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
            pairs = zip(k[11 - len(inn):], [int(x) for x in inn])
            return str(sum([k * v for k, v in pairs]) % 11 % 10)

        if len(inn) == 10:
            if inn[-1] == inn_csum(inn[:-1]):
                return inn
            else:
                raise ValidationError("Неверный ИНН")
        else:
            if inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1]):
                return inn
            else:
                raise ValidationError("Неверный ИНН")

    class Meta:
        model = Seller
        fields = ['itn', 'phone']


class AdForm(ModelForm):

    class Meta:
        model = Ad
        fields = ['name', 'description', 'category', 'tag', 'price']


class SMSLogForm(ModelForm):

    class Meta:
        model = SMSLog
        fields = ['code']


ImageFormset = inlineformset_factory(Ad, Picture, fields=('image',), extra=1)
