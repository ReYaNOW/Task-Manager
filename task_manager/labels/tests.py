from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import SetUpLoggedUserMixin
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TestLabelsMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_label = Label.objects.create(name='name')
        cls.test_form_data = {'name': 'Tota_label'}


class TestLabelListView(SetUpLoggedUserMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('labels_list')

    def test_index_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class TestLabelCreate(TestLabelsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('label_create')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        before_creation = Label.objects.count()
        response = self.client.post(self.url, data=self.test_form_data)

        self.assertTrue(Label.objects.count() == before_creation + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_list'))


class TestLabelUpdate(TestLabelsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('label_update', args=[cls.test_label.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url, data=self.test_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_list'))

        updated_label = Label.objects.get(id=self.test_label.id)
        self.assertEqual(updated_label.name, self.test_form_data['name'])


class TestLabelDelete(TestLabelsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('label_delete', args=[cls.test_label.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_list'))

        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=self.test_label.id)


class TestLabelDeleteLinked(TestLabelsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.other_user = get_user_model().objects.create(
            username='Tota', password='SuperTota'
        )
        cls.test_status = Status.objects.create(name='Test status')
        cls.test_task = Task.objects.create(
            name='Test task',
            status=cls.test_status,
            author=cls.other_user,
        )
        cls.test_task.labels.set([cls.test_label])

        cls.url = reverse('label_delete', args=[cls.test_label.id])

    def test_label_delete_linked(self):
        before_deletion = len(Label.objects.all())
        self.client.post(self.url)
        after_deletion = len(Label.objects.all())
        self.assertTrue(before_deletion == after_deletion)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message=_('label_in_usage'),
        )
