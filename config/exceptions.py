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


# def return_serializer_data_or_error(_serializer: Any) -> Any:
#     """Return Valid serializer data else return error."""
#     if _serializer.is_valid():
#         return _serializer
#     else:
#         # print(_serializer.errors)
#         # error handling
#         try:
#             key = list(_serializer.errors.keys())[0]
#             value = list(_serializer.errors.values())[0]
#             code = re.search("code=['a-z]+", str(value)).group()
#             if "required" in code:
#                 value = _serializer.errors[key][0]
#                 message = "{}{}".format(key, value.replace("This", ""))
#             elif "blank" in code:
#                 value = _serializer.errors[key][0]
#                 message = "{}{}".format(key, value.replace("This", ""))
#             elif "invalid" in code:
#                 message = re.search(r"string=\'([A-Za-z\s.]+)", str(value)).groups()[0]
#             elif "null" in code:
#                 message = f"{key} is required"
#                 # print("my message", message)
#                 # raise CustomValidation({'error': f"{key} is required"})
#             else:
#                 message = _serializer.errors[key][0]
#         except Exception as e:
#             log.info("Exception {}: ".format(str(e)))
#             try:
#                 string = str(_serializer.errors)
#                 message = (
#                     re.search("string='(?P<error>[a-z ]+)", string)
#                     .groupdict()
#                     .get("error")
#                 )
#                 message = message.replace("This field", key)
#             except Exception:
#                 # raise CustomValidation({'error': list(_serializer.errors.values())[0]})

#                 raise CustomValidation({"errors": _serializer.errors})

#         raise CustomValidation(
#             {"error": message if message else _serializer.errors}, 400
#         )
