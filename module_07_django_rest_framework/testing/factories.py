import factory
from faker import Faker
from django.contrib.auth.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyFunction(lambda: fake.unique.user_name())
    email = factory.LazyFunction(lambda: fake.unique.email())
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class AdminFactory(UserFactory):
    is_staff = True
    is_superuser = True


# class AuthorFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Author
#     first_name = factory.LazyFunction(fake.first_name)
#     last_name = factory.LazyFunction(fake.last_name)
#     email = factory.LazyFunction(lambda: fake.unique.email())

# class BookFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Book
#     title = factory.LazyFunction(fake.catch_phrase)
#     pages = factory.LazyFunction(lambda: fake.random_int(50, 800))
#     price = factory.LazyFunction(lambda: round(fake.random.uniform(9.99, 49.99), 2))
#     author = factory.SubFactory(AuthorFactory)
#     status = "published"