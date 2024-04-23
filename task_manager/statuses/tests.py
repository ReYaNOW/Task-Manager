from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.mixins import SetUpLoggedUserMixin
from task_manager.statuses.models import Status


class TestStatusesMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_status = Status.objects.create(name='name')
        cls.test_form_data = {'name': 'Tota_status'}


class TestStatusListView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('statuses_list')

    def test_index_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class TestStatusCreate(TestStatusesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('status_create')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        before_creation = Status.objects.count()
        response = self.client.post(self.url, data=self.test_form_data)

        self.assertTrue(Status.objects.count() == before_creation + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))


class TestStatusUpdate(TestStatusesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('status_update', args=[cls.test_status.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url, data=self.test_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))

        updated_status = Status.objects.get(id=self.test_status.id)

        self.assertEqual(updated_status.name, self.test_form_data['name'])


class TestStatusDelete(TestStatusesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('status_delete', args=[cls.test_status.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=self.test_status.id)
