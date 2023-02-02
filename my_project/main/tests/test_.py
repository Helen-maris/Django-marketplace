from django.test import TestCase
import pytest

from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Seller, Category, Ad


# TestCase
class ViewResponses(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username="user", email="testuser@example.com", password="qwerty")
        test_seller = Seller.objects.create(user=test_user)
        test_category = Category.objects.create(name="electronics")
        Ad.objects.create(
            name='Ad', description='New test ad',
            category=test_category, seller=test_seller)

    def test_ads(self):
        response = self.client.get(reverse('ad-list'))
        self.assertEqual(response.status_code, 200)

    def test_myads(self):
        response = self.client.get(reverse('my-ads'))
        self.assertRedirects(response, '/accounts/login/?next=/my_ads/')

        self.client.login(username="user", password="qwerty")
        response = self.client.get(reverse('my-ads'))
        self.assertEqual(response.status_code, 200)

    def test_ad_detail(self):
        response = self.client.get(reverse('ad-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_seller_upd(self):
        response = self.client.get(reverse('seller-update'))
        redirects_to = '/accounts/login/?next=/accounts/seller/'
        self.assertRedirects(response, redirects_to)

        self.client.login(username="user", password="qwerty")
        response = self.client.get(reverse('seller-update'))
        self.assertEqual(response.status_code, 200)

    def test_create_ad(self):
        response = self.client.get(reverse('ad-create'))
        self.assertRedirects(response, '/accounts/login/?next=/ads/add/')

        self.client.login(username="user", password="qwerty")
        response = self.client.get(reverse('ad-create'))
        self.assertEqual(response.status_code, 200)

    def test_ad_update(self):
        self.client.login(username="user", password="qwerty")
        response = self.client.get(reverse('ad-update', args=[1]))
        self.assertEqual(response.status_code, 200)


# pytest
@pytest.fixture
def auto_login_user(client, db, django_user_model):
    def make_auto_login():
        user = django_user_model.objects.create_user(
            username="user", email="testuser@example.com", password="qwerty")
        client.login(username="user", password="qwerty")
        return client, user
    return make_auto_login


@pytest.fixture
def new_objects(db, auto_login_user):
    def create_objects():
        client, test_user = auto_login_user()
        test_seller = Seller.objects.create(user=test_user)
        test_category = Category.objects.create(name="electronics")
        Ad.objects.create(
            name='Ad', description='New test ad',
            category=test_category, seller=test_seller)
        return client
    return create_objects


@pytest.mark.django_db
def test_ads(client):
    response = client.get(reverse('ad-list'))
    assert response.status_code == 200


def test_myads(auto_login_user):
    client, user = auto_login_user()
    response = client.get(reverse('my-ads'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_ad_detail(new_objects):
    client = new_objects()
    response = client.get(reverse('ad-detail', args=[1]))
    assert response.status_code == 200


def test_create_ad(auto_login_user):
    client, user = auto_login_user()
    response = client.get(reverse('ad-create'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_ad_update(new_objects):
    client = new_objects()
    response = client.get(reverse('ad-update', args=[1]))
    assert response.status_code == 200
