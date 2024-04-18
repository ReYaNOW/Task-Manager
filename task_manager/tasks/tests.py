from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class CustomTestCase(TestCase):
    fixtures = ['tasks.json', 'labels.json', 'statuses.json', 'users.json']

    test_task = {
        'name': 'Task for Tota',
        'description': 'Task description for Tota',
        'status': 1,
        'executor': 1,
        'labels': [1, 2],
    }

    def setUp(self):
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)

        self.status1 = Status.objects.get(pk=4)
        self.status2 = Status.objects.get(pk=8)
        self.status3 = Status.objects.get(pk=9)

        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)

        self.client: Client = Client()
        self.client.force_login(self.user1)


class TaskCreate(CustomTestCase):
    def test_get(self):
        response = self.client.get(reverse('task_create'))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        params = self.test_task
        before_creation = Task.objects.count()
        response = self.client.post(reverse('task_create'), data=params)

        self.assertTrue(Task.objects.count() == before_creation + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))


class TaskUpdate(CustomTestCase):
    def test_get(self):
        response = self.client.get(
            reverse('task_update', args=[self.task1.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        params = self.test_task
        response = self.client.post(
            reverse('task_update', args=[self.task1.id]), data=params
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))

        updated_task = Task.objects.get(id=self.task1.id)

        self.assertEqual(updated_task.name, params['name'])


class TaskDelete(CustomTestCase):
    def test_get(self):
        response = self.client.get(
            reverse('task_delete', args=[self.task1.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        before_deletion = len(Task.objects.all())
        response = self.client.post(
            reverse('task_delete', args=[self.task1.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=self.task1.id)

        after_deletion = len(Task.objects.all())
        self.assertTrue(before_deletion == after_deletion + 1)

    def test_delete_not_author(self):
        before_deletion = len(Task.objects.all())
        self.client.post(reverse('task_delete', args=[self.task2.id]))
        after_deletion = len(Task.objects.all())

        self.assertTrue(before_deletion == after_deletion)
        self.assertRaisesMessage(
            expected_exception=PermissionDenied,
            expected_message=_('task_no_permissions'),
        )


class TaskDetail(CustomTestCase):
    def test_task_detail(self):
        response = self.client.get(reverse('task_read', args=[self.task2.pk]))

        self.assertEqual(response.status_code, 200)


class TaskFilter(CustomTestCase):
    def test_filter_by_status(self):
        response = self.client.get(
            reverse('tasks_index'),
            {'status': self.status1.pk}
        )
        tasks = response.context['tasks']
        
        self.assertEqual(tasks.count(), 1)
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.task1, tasks)
        self.assertNotIn(self.task3, tasks)
    
    def test_filter_by_label(self):
        response = self.client.get(
            reverse('tasks_index'),
            {'labels': self.label3.pk}
        )
        tasks = response.context['tasks']
        
        self.assertEqual(tasks.count(), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.task3, tasks)
    
    def test_filter_by_current_user(self):
        response = self.client.get(reverse('tasks_index'), {'personal': 'on'})
        tasks = response.context['tasks']
        
        self.assertEqual(tasks.count(), 1)
        self.assertIn(self.task1, tasks)
        self.assertNotIn(self.task2, tasks)
        self.assertNotIn(self.task3, tasks)
