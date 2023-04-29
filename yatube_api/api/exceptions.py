from django.core.exceptions import ValidationError


class FollowError(ValidationError):
    """Error with follow."""
    pass
