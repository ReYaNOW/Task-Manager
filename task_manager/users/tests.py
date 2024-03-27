from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse


def get_test_user_data():
    return {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'password': 'password',
    }


def get_test_user_form_data():
    return {
        'username': 'Tota',
        'first_name': 'To',
        'last_name': 'Ta',
        'password1': 'TotaTota',
        'password2': 'TotaTota',
    }


class CustomTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        test_user = get_test_user_data()
        self.test_user = User.objects.create_user(**test_user)
        test_user['username'] = 'username2'
        self.test_user2 = User.objects.create_user(**test_user)


class UsersCreate(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user_data = get_test_user_form_data()
        response = self.client.post(reverse('user_create'), data=user_data)

        self.assertTrue(User.objects.get(id=1))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class UsersUpdate(CustomTestCase):
    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse('user_update', args=[self.test_user.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_user_update_without_auth(self):
        test_user = get_test_user_form_data()
        self.client.post(reverse('user_create'), data=test_user)
        response = self.client.get(
            reverse('user_update', args=[self.test_user.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_update_other_user(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse('user_update', args=[self.test_user2.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))

    def test_post(self):
        self.client.force_login(self.test_user)
        params = get_test_user_form_data()
        response = self.client.post(
            reverse('user_update', args=[self.test_user.id]), data=params
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))

        updated_user = User.objects.get(id=self.test_user.id)

        self.assertEqual(updated_user.username, params['username'])
        self.assertEqual(updated_user.first_name, params['first_name'])
        self.assertEqual(updated_user.last_name, params['last_name'])


class UsersDelete(CustomTestCase):
    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse('user_delete', args=[self.test_user.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.test_user2)
        response = self.client.post(
            reverse('user_delete', args=[self.test_user2.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=self.test_user2.id)
