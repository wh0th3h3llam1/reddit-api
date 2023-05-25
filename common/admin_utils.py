def FieldSets(**kwargs) -> list:
    """
    A small utility to simplify the use of fieldsets in Admin.
    It will create different sections for each key provided.

    Usage:
    ```
    class MyModelAdmin(admin.ModelAdmin):
        fieldsets = FieldSets(
            none=("username", "password"),
            personal_info=(
                "first_name", "last_name", "email", "phone_number",
                "location", "profile_image"
            ),
            permissions=(
                "is_active",
                "is_staff",
                "is_superuser",
            ),
            important_dates=("last_login", "date_joined"),
        )
    ```
    """

    sections = []

    for key, value in kwargs.items():
        key = None if key.lower() == "none" else key.replace("_", " ").title()

        sections.append((key, {"fields": value}))

    return sections
