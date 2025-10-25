from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import Optional


class CustomUser(AbstractUser):
    """Custom user model with additional fields."""

    # Basic user info
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    # User preferences
    source = models.CharField(
        max_length=50,
        blank=True,
        help_text="How the user found out about the service (e.g., 'google', 'twitter', 'friend')"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    @property
    def can_create_capture(self) -> bool:
        """Check if user can create a new capture (always true for free users)."""
        return True

    @property
    def get_remaining_free_captures(self) -> int:
        """Get remaining free captures (unlimited for free users)."""
        return 999999  # Effectively unlimited

    class Meta:
        db_table = "custom_user"