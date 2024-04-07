import pyotp
# Django
from django.db import models
from django.contrib.auth.models import User
# Models
from apps.common import models as base_model


class Profile(base_model.BaseModelNotRef):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile',
        null=False,
        blank=False

    )
    ROLES = (
        ('Administrator', 'Administrator'),
        ('Client', 'Client'),
        ('User', 'User'),
    )
    role = models.CharField(
        'Role',
        choices=ROLES,
        max_length=20,
        null=False,
        blank=False
    )
    photo_url = models.ImageField(
        upload_to='users/',
        verbose_name='Profile Photo',
        null=True,
        blank=True,
    )
    completed = models.BooleanField(
        'Completed',
        default=False
    )
    email_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email address.'
    )
    terms_policy = models.BooleanField(
        'Terms & Policy',
        default=False,
        help_text='Set to true when the user accepted conditions and policy.'
    )
    o_key = models.BinaryField(
        'OTP key',
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        """Return username."""
        return str(self.user)
