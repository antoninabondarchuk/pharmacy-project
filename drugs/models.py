from django.db import models
from firms.models import UUIDClass


class InternationalName(UUIDClass):
    name = models.TextField(null=True)


class MarketingStatus(UUIDClass):
    name = models.TextField(null=True)


class PharmacotherapeuticGroup(UUIDClass):
    name = models.TextField(null=True)


class ATC(UUIDClass):
    name = models.CharField(max_length=20, null=True)
    type = models.IntegerField(null=True)


class DrugType(UUIDClass):
    name = models.CharField(max_length=100, null=True)


class INN(UUIDClass):
    name = models.CharField(max_length=50, null=True)


class PrematureTermination(UUIDClass):
    date = models.DateField(null=True)
    reason = models.TextField(null=True)
