from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.statuses.models import Status


def get_test_status_data():
    return {'name': 'name'}


def get_test_status_form_data():
    return {'name': 'Tota_status'}


class CustomTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        test_user_data = {
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': 'password',
        }
        self.test_user = User.objects.create_user(**test_user_data)

        test_status = get_test_status_data()
        self.test_status1 = Status.objects.create(**test_status)
        test_status['name'] = 'name2'
        self.test_status2 = Status.objects.create(**test_status)


class StatusCreate(CustomTestCase):
    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('status_create'))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.test_user)
        status_data = get_test_status_form_data()
        before_creation = Status.objects.count()
        response = self.client.post(reverse('status_create'), data=status_data)

        self.assertTrue(Status.objects.count() == before_creation + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))


class StatusUpdate(CustomTestCase):
    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse('status_update', args=[self.test_status1.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.test_user)
        params = get_test_status_form_data()
        response = self.client.post(
            reverse('status_update', args=[self.test_status1.id]), data=params
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))

        updated_status = Status.objects.get(id=self.test_status1.id)

        self.assertEqual(updated_status.name, params['name'])


class StatusDelete(CustomTestCase):
    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse('status_delete', args=[self.test_status1.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.test_user)
        response = self.client.post(
            reverse('status_delete', args=[self.test_status2.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=self.test_status2.id)
