from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def username_validator(username: str) -> str:
    if username is None:
        raise ValidationError("Username cannot be empty")
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    regex = ""

    if username.startswith(""):
        raise ValidationError("Username can't start with ")

    if not any(char for char in username):
        raise ValidationError(
            "Username can have only letters, numbers and -/_/. characters"
        )
    return username


def subreddit_validator(name: str) -> str:
    return name


class UsernameValidator(RegexValidator):
    flags = 0
    message = ""
    regex = ""
