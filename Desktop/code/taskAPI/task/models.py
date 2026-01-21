from django.db import models
from django.conf import settings


# Create your models here.
User = settings.AUTH_USER_MODEL


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
