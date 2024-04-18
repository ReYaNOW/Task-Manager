from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label


def get_test_label_data():
    return {'name': 'name'}


def get_test_label_form_data():
    return {'name': 'Tota_label'}


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

        test_label = get_test_label_data()
        self.test_label1 = Label.objects.create(**test_label)
        test_label['name'] = 'name2'
        self.test_label2 = Label.objects.create(**test_label)


class LabelCreate(CustomTestCase):
    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('label_create'))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.test_user)
        label_data = get_test_label_form_data()
        before_creation = Label.objects.count()
        response = self.client.post(reverse('label_create'), data=label_data)

        self.assertTrue(Label.objects.count() == before_creation + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))


class LabelUpdate(CustomTestCase):
    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse('label_update', args=[self.test_label1.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.test_user)
        params = get_test_label_form_data()
        response = self.client.post(
            reverse('label_update', args=[self.test_label1.id]), data=params
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))

        updated_label = Label.objects.get(id=self.test_label1.id)

        self.assertEqual(updated_label.name, params['name'])


class LabelDelete(CustomTestCase):
    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse('label_delete', args=[self.test_label1.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.test_user)
        response = self.client.post(
            reverse('label_delete', args=[self.test_label2.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=self.test_label2.id)

    def test_status_delete_linked(self):
        before_deletion = len(Label.objects.all())
        self.client.post(reverse('label_delete', args=[self.test_label2.id]))
        after_deletion = len(Label.objects.all())
        self.assertTrue(before_deletion == after_deletion)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message=_('label_in_usage'),
        )
