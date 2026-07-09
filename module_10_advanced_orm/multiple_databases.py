"""Multiple databases and database routers.

Docs: https://docs.djangoproject.com/en/stable/topics/db/multi-db/
"""


class PrimaryReplicaRouter:
    """Reads go to a replica, writes go to the primary."""

    def db_for_read(self, model, **hints):
        return "replica"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"


# settings.py:
#   DATABASES = {"default": {...primary...}, "replica": {...read replica...}}
#   DATABASE_ROUTERS = ["myapp.routers.PrimaryReplicaRouter"]

# Manual selection bypasses the router:
#   Article.objects.using("replica").all()
#   article.save(using="default")