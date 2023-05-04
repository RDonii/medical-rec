from django.contrib.auth.models import AbstractUser


# Overriding default User model to avoid future migration conflicts: https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-AUTH_USER_MODEL
class User(AbstractUser):
    pass
