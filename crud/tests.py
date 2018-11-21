import datetime
import pytz

from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK

from crud.models import Todo

TZ = pytz.timezone('US/Pacific')


class TodoTest(TestCase):
    """Ok, these tests could be more complete, but they really are just filler."""

    def setUp(self):
        Todo.objects.create(
            text='A test todo',
            state='DN',
            due_at=datetime.datetime.now(tz=TZ)
        )
        self.client = APIClient()

    def test_created(self):
        first_todo = Todo.objects.get(text='A test todo')
        self.assertEqual(first_todo.state, 'DN')

    def test_list_view(self):
        response = self.client.get(reverse_lazy('view:list_view'))
        self.assertEqual(response.status_code, HTTP_200_OK)
