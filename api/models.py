from django.db import models
from django.conf import settings


class Profile(models.Model):
    company_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Patient(models.Model):
    class GenderChoice(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    first_name = models.CharField(max_length=150, db_index=True)
    last_name = models.CharField(max_length=150, db_index=True)
    birth_date = models.DateField(null=True, blank=True, db_index=True)
    gender = models.CharField(max_length=1, choices=GenderChoice.choices, null=True, blank=True)
    med_condition = models.TextField()
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patients')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['updated', 'first_name', 'last_name']


class Material(models.Model):
    file = models.FileField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
