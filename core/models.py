from django.contrib.auth.models import AbstractUser


# Overriding default User model to avoid future migration conflicts
class User(AbstractUser):
    pass
