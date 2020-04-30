import uuid
from django.db import models


class UUIDClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Country(UUIDClass):
    name = models.CharField(max_length=100, null=True)


class Manufacturer(UUIDClass):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    name = models.TextField(null=True)
    address = models.TextField(null=True)


class Applicant(UUIDClass):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    name = models.TextField(null=True)
    address = models.TextField(null=True)
