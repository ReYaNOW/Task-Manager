from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.mixins import SetUpLoggedUserMixin


class TestUsersMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_data = {
            'username': 'username2',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': 'password',
        }
        cls.test_user2 = get_user_model().objects.create_user(**cls.test_data)

        cls.test_form_data = {
            'username': 'Tota',
            'first_name': 'To',
            'last_name': 'Ta',
            'password1': 'TotaTota',
            'password2': 'TotaTota',
        }


class TestUserListView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('users_list')

    def test_index_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestUsersCreate(TestUsersMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('user_create')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        before_create = get_user_model().objects.count()
        response = self.client.post(self.url, data=self.test_form_data)

        self.assertTrue(get_user_model().objects.count() == before_create + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class TestUsersUpdate(TestUsersMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('user_update', args=[cls.logged_user.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_update_without_auth(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_update_other_user(self):
        response = self.client.get(
            reverse('user_update', args=[self.test_user2.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

    def test_post(self):
        response = self.client.post(self.url, data=self.test_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))

        updated_user = get_user_model().objects.get(id=self.logged_user.id)
        params = self.test_form_data

        self.assertEqual(updated_user.username, params['username'])
        self.assertEqual(updated_user.first_name, params['first_name'])
        self.assertEqual(updated_user.last_name, params['last_name'])


class TestUsersDelete(TestUsersMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('user_delete', args=[cls.logged_user.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(id=self.logged_user.id)
