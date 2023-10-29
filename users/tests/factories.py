from django.core.files.base import ContentFile

import factory
from faker import Faker
from allauth.account.models import EmailAddress

from users.models import User

# Create your factories here.

fake = Faker()
Faker.seed(0)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # username = factory.build(
    #     klass=dict,
    #     user=factory.Faker("user_name"),
    # )["user_name"]
    # email = fake.ascii_email()
    username = "admin"
    email = "admin@mail.co"
    password = factory.django.Password("random_password")
    phone_number = fake.phone_number()
    avatar = factory.LazyAttribute(
        lambda _: ContentFile(
            content=factory.django.ImageField()._make_data(
                {"width": 500, "height": 500}
            ),
            name="example.jpg",
        )
    )
    deactivated_on = None
    is_active = True


class EmailAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailAddress

    user = factory.SubFactory(UserFactory)
    email = fake.ascii_email()
    verified = False
    primary = False
