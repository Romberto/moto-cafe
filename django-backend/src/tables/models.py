from django.contrib.auth.models import User
from django.db import models


class TableModel(models.Model):
    name = models.CharField(max_length=100)
    owner_officiant = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f"{self.id}:{self.name}"
