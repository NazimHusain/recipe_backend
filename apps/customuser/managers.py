from django.contrib.auth.models import BaseUserManager
from typing import Any, Optional


class CustomUserManager(BaseUserManager):
    """Model manager for User model."""

    def _create_user(
            self: 'CustomUserManager',
            email: str,
            password: str = None,
            **extra_fields: dict
            ) -> Any:
        """Create and save a User with the given email and password."""

        email = self.normalize_email(email)
        extra_fields.pop("username", None)
        user = self.model(
            username=email, email=email, password=password, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self: 'CustomUserManager',
            username: str,
            email: Optional[str] = None,
            password: Optional[str] = None,
            **extra_fields: dict
            ) -> Any:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(
            self: 'CustomUserManager',
            email: str,
            password: Optional[str] = None,
            **extra_fields: dict
            ) -> Any:
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", 1)
        # extra_fields.setdefault("username", email.split("@")[0])

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
