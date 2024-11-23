from rest_framework import serializers
from typing import Any, Union
from apps.customuser import models as UserModels
from config.exceptions import CustomValidation

class UserLoginSerializer(serializers.Serializer):
    """Serializer for User's login."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self: 'UserLoginSerializer', attrs: dict) -> Union[dict, CustomValidation]:
        username = attrs["username"]
        password = attrs["password"]
        self.user = UserModels.User.objects.filter(email=username, is_active=True).first()
        if self.user and self.user.check_password(password):
            return attrs
        else:
            raise CustomValidation("Invalid Credentials", 400)
        


