from django.db import models
from django.conf import settings


class Profile(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']