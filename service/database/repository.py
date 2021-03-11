"""
Implements the repository pattern inside django.
"""
from service.database.abstract_repository import AbstractRepository


class Repository(AbstractRepository):
    """Repository

    A repository that implements the Django models.

    Args:
        Model (django.db.model): the model bound to this repository
    """

    def __init__(self, model=None):
        self.model = model
        self.objects = model.objects

    def get(self, id):
        return self.model.objects.get(id=id)

    def get_by(self, **kwargs):
        return self.model.objects.filter(**kwargs).first()

    def all(self):
        return self.model.objects.all()

    def all_by(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def add(self, entity):
        entity.save()

    def update(self, entity):
        entity.save()

    def remove(self, entity):
        entity.delete()

    def save(self):
        pass
