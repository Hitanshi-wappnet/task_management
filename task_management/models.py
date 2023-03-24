from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    """
    Task Model which contains title,description,created_date,due_date
    and user field.
    """
    class Meta:
        ordering = ["due_date"]

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Manager(models.Model):

    """
    Manager Model which contains manager,Task and employee field.
    """
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    Task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.CharField(max_length=50, default=None)
