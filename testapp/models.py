from django.db import models
from django.db.models.signals import post_save

from cometgw.methods import send


class ToDo(models.Model):
    description = models.TextField()
    due = models.DateTimeField()


def on_new_todo(sender, instance, **kwargs):
    send('myexchange', 'myroute',
         {'description' : instance.description,
          'due' : str(instance.due) })

models.signals.post_save.connect(on_new_todo, sender=ToDo)
