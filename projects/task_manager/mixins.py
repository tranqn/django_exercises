"""Reusable view mixins."""


class OwnerQuerysetMixin:
    """Limit the queryset to objects owned by the current user.

    Stops users from viewing or editing each other's rows by guessing the
    URL pk — a missing row returns 404, which also avoids leaking existence.
    """

    owner_field = "owner"

    def get_queryset(self):
        return super().get_queryset().filter(**{self.owner_field: self.request.user})