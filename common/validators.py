from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


SPECIAL_CHARACTERS = "[~\!@#\$%\^&\*\(\)\+{}\":;'\[\]]"

def username_validator(username: str) -> str:
    if username is None:
        raise ValidationError("Username cannot be empty")

    if not (5 <= len(username) <= 30):
        raise ValidationError(
            "Username length must be between 5 and 30 characters"
        )

    if " " in username:
        raise ValidationError("Username may not contain `space`")

    if not username[0].isalpha():
        raise ValidationError("Username must start with characters")

    if not username[-1].isalnum():
        raise ValidationError("Username must end with alphanumeric characters")

    if any(char in SPECIAL_CHARACTERS for char in username):
        raise ValidationError(
            "Username can have only letters, numbers and _/. characters"
        )
    return username


def subreddit_validator(name: str) -> str:
    return name
