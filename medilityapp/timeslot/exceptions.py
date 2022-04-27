from rest_framework.exceptions import APIException


class DateNotAvailable(APIException):
    status_code = 400
    default_detail = "Selected date is not available."
    default_code = "date_not_available"