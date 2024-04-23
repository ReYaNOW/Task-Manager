from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.mixins import SetUpLoggedUserMixin
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TestTasksMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_status = Status.objects.create(name='Test status')
        cls.logged_user_task = Task.objects.create(
            name='Test task', status=cls.test_status, author=cls.logged_user
        )
        cls.test_label = Label.objects.create(name='name')
        cls.logged_user_task.labels.set([cls.test_label])

        cls.other_user = get_user_model().objects.create(
            username='Tota', password='SuperTota'
        )


class TestCreateUpdateMixin(TestTasksMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_form_data = {
            'name': 'Task for Tota',
            'description': 'Task description for Tota',
            'status': cls.test_status.id,
            'executor': cls.logged_user.id,
            'labels': [cls.test_label.id],
        }


class TestTaskDetailView(TestTasksMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('task_read', args=[cls.logged_user_task.id])

    def test_task_detail_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_detail_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))


class TestTaskCreate(TestCreateUpdateMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('task_create')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        before_creation = Task.objects.count()
        response = self.client.post(self.url, data=self.test_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTrue(Task.objects.count() == before_creation + 1)


class TestTaskUpdate(TestCreateUpdateMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('task_update', args=[cls.logged_user_task.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.url, data=self.test_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))

        updated_task = Task.objects.get(id=self.logged_user_task.id)
        self.assertEqual(updated_task.name, self.test_form_data['name'])


class TestTaskDelete(TestTasksMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse('task_delete', args=[cls.logged_user_task.id])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        before_deletion = len(Task.objects.all())
        response = self.client.post(self.url)

        after_deletion = len(Task.objects.all())
        self.assertTrue(before_deletion == after_deletion + 1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=self.logged_user_task.id)

    def test_delete_not_author(self):
        self.client.force_login(self.other_user)
        before_deletion = len(Task.objects.all())
        self.client.post(self.url)
        after_deletion = len(Task.objects.all())

        self.assertTrue(before_deletion == after_deletion)
        self.assertRaisesMessage(
            expected_exception=PermissionDenied,
            expected_message=_('task_no_permissions'),
        )


class TestLoggedUserAndTaskFilterView(TestTasksMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.other_status = Status.objects.create(name='Other test status')
        cls.other_user = get_user_model().objects.create(
            username='alexander_the_great', password='qwer1234qwer1234'
        )

        cls.other_task = Task.objects.create(
            name='other task',
            status=cls.other_status,
            author=cls.other_user,
        )
        cls.url = reverse('tasks_list')

    def test_task_filter_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            list(response.context['tasks']), Task.objects.all()
        )

    def test_task_filter_view_get_by_status(self):
        filter_param_test_status = {'status': self.test_status.pk}
        response = self.client.get(self.url, data=filter_param_test_status)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(**filter_param_test_status),
        )

    def test_task_filter_view_get_by_executor(self):
        self.logged_user_task.executor = self.logged_user
        self.logged_user_task.save()

        filter_param_executor = {'executor': self.logged_user.pk}
        response = self.client.get(self.url, data=filter_param_executor)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(**filter_param_executor),
        )

    def test_task_filter_view_get_by_label(self):
        test_label = Label.objects.create(name='Test label')
        self.logged_user_task.labels.set([test_label])

        filter_param_label = {'labels': test_label.pk}
        response = self.client.get(self.url, data=filter_param_label)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.filter(labels__in=[test_label]),
        )

    def test_task_filter_view_get_by_own_tasks(self):
        filter_param_own_tasks = {'personal': 'on'}
        response = self.client.get(self.url, data=filter_param_own_tasks)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['tasks'], [self.logged_user_task]
        )

    def test_status_filter_view_get_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))
