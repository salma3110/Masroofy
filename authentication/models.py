from django.db import models

"""
@file authentication/models.py
@brief Models for authentication app (User storage).

This module contains the `User` model used to store a single application's
user with a hashed PIN and lockout metadata.

@author Masroofy
"""

class User(models.Model):
    """
    @brief Simple user model for PIN-based authentication.

    @var name Unique username for the account
    @var pin Hashed PIN string
    @var failed_attempts Number of consecutive failed login attempts
    @var is_locked Whether the account is currently locked
    @var lock_time Timestamp when the account was locked
    """
    name = models.CharField(max_length=100, unique=True)
    pin = models.CharField(max_length=255)
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    lock_time = models.DateTimeField(null=True, blank=True)
