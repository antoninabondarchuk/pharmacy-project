from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from drugs.models import ATC
from firms.models import Applicant, Manufacturer, Country


@registry.register_document
class ApplicantDocument(Document):
    name = fields.TextField()
    address = fields.TextField()
    country = fields.ObjectField(
        properties={
            'name': fields.TextField()
        }
    )

    class Index:
        name = 'applicants'

    class Django:
        model = Applicant
        related_models = [Country, ]

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, ATC):
            return related_instance.atcs_set.all()
        return []


@registry.register_document
class ManufacturerDocument(Document):
    name = fields.TextField()
    address = fields.TextField()
    country = fields.ObjectField(
        properties={
            'name': fields.TextField()
        }
    )

    class Index:
        name = 'manufacturers'

    class Django:
        model = Manufacturer
        related_models = [Country, ]

    def get_queryset(self):
        return super(ManufacturerDocument, self).get_queryset().select_related(
            'country_id',
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Country instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Country):
            return related_instance.manufacturer_set.all()
        return []


@registry.register_document
class CountryDocument(Document):
    name = fields.TextField()

    class Index:
        name = 'countries'

    class Django:
        model = Country
