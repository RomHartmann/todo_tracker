from django.utils import timezone
from django.db import models


class Todo(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    state = models.CharField(
        max_length=2,
        choices=(('TD', 'todo'), ('IP', 'in-progress'), ('DN', 'done')),
        default='TD',
    )
    due_at = models.DateTimeField(null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return "{}:{}".format(self.get_state_display(), self.text[0:20])
