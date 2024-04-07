from django_tenants.routers import TenantSyncRouter


# noinspection PyArgumentList
class PrimaryReplicaRouter(TenantSyncRouter):
    """
    An example primary/replica router adapted from:
    https://docs.djangoproject.com/en/3.1/topics/db/multi-db/
    """
    def db_for_read(self, model, **hints):
        """
        Reads go to the replica.
        """
        return 'replica'

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {'default', 'replica'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None