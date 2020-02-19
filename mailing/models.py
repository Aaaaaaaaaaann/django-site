from django.db import models


class Follower(models.Model):
    email = models.EmailField(unique=True)
    activated = models.BooleanField(default=False)
    joined = models.DateField(null=True, blank=True)
    unsubscribed = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.email
