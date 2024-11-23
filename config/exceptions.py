from rest_framework.exceptions import APIException
import re
from typing import Any, Optional


class CustomValidation(APIException):
    """Own defined Validation."""

    default_status_code = 400

    def __init__(
        self: "CustomValidation", detail: Any, status_code: Optional[int] = None
    ) -> Any:
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = self.default_status_code
        self.detail = detail

