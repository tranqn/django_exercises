"""factory_boy factories for fast, readable test data.

    from .factories import UserFactory
    user = UserFactory()                 # one user
    users = UserFactory.create_batch(5)  # five users
"""
import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    is_active = True

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        obj.set_password(extracted or "password123")
        if create:
            obj.save()