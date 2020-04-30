from django_elasticsearch_dsl.registries import registry
from drugs.drug_model import Drug
from firms.models import Manufacturer, Applicant
from drugs.models import InternationalName, MarketingStatus, PharmacotherapeuticGroup, ATC, DrugType, INN, \
    PrematureTermination
from django_elasticsearch_dsl import fields, Document


@registry.register_document
class ATCDocument(Document):
    name = fields.TextField()
    type = fields.IntegerField()

    class Index:
        name = 'atcs'

    class Django:
        model = ATC


@registry.register_document
class DrugDocument(Document):
    source_id = fields.TextField(
        fields={
            'raw': fields.KeywordField()
        }
    )
    trade_name = fields.TextField(
        fields={
            'raw': fields.KeywordField(),
        },
    )
    international_name = fields.ObjectField(
        properties={
            'name': fields.TextField(
                fields={
                    'raw': fields.KeywordField(),
                }
            )
        }
    )
    drug_form = fields.TextField()
    marketing_status = fields.ObjectField(
        properties={
            'name': fields.TextField(
                fields={
                    'raw': fields.KeywordField(),
                }
            )
        }
    )
    formula = fields.TextField()
    pharmacotherapeutic_group = fields.ObjectField(
        properties={
            'name': fields.TextField()
        }
    )
    atcs = fields.NestedField(
        properties={
            'name': fields.TextField(),
            'type': fields.IntegerField()
        }
    )
    drug_applicant = fields.ObjectField(
        properties={
            'name': fields.TextField(),
            'address': fields.TextField(),
            'country_id': fields.ObjectField(
                properties={
                    'name': fields.TextField()
                }
            )
        }
    )
    manufacturers = fields.NestedField(
        properties={
            'name': fields.TextField(),
            'address': fields.TextField(),
            'country_id': fields.ObjectField(
                properties={
                    'name': fields.TextField()
                }
            )
        }
    )
    registration_number = fields.TextField(
        fields={
            'raw': fields.KeywordField()
        }
    )
    registration_date = fields.DateField()
    expiration_date = fields.TextField()
    drug_type = fields.ObjectField(
        properties={
            'name': fields.TextField()
        }
    )
    has_bio_origin = fields.BooleanField()
    has_phyto_origin = fields.BooleanField()
    is_orphan = fields.BooleanField()
    is_homeopatic = fields.BooleanField()
    INN = fields.ObjectField(
        properties={
            'name': fields.TextField()
        }
    )
    premature_termination = fields.ObjectField(
        properties={
            'date': fields.DateField(),
            'reason': fields.TextField()
        }
    )
    instruction_url = fields.KeywordField()

    class Django:
        model = Drug  # The model associated with this Document
        queryset_pagination = 20
        related_models = [Manufacturer, InternationalName, MarketingStatus, PharmacotherapeuticGroup, ATC, Applicant,
                          DrugType, INN, PrematureTermination]

    class Index:
        name = 'drugs'

    class Meta:
        ordering = ('trade_name', )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the ATC instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, ATC):
            return related_instance.atcs_set.all()

    def get_queryset(self):
        """
        Using for getting results with nested docs in one request.
        """
        return super(DrugDocument, self).get_queryset().select_related(
            'international_name', 'marketing_status',
            'pharmacotherapeutic_group', 'drug_applicant',
            'drug_type', 'INN', 'premature_termination',
        )


@registry.register_document
class InternationalNameDocument(Document):
    name = fields.TextField()

    class Index:
        name = 'international_names'

    class Django:
        model = InternationalName


@registry.register_document
class MarketingStatusDocument(Document):
    name = fields.TextField()

    class Index:
        name = 'marketing_statuses'

    class Django:
        model = MarketingStatus


@registry.register_document
class PharmacotherapeuticGroupDocument(Document):
    name = fields.TextField()

    class Index:
        name = 'pharmacotherapeutic_groups'

    class Django:
        model = PharmacotherapeuticGroup


@registry.register_document
class DrugTypeDocument(Document):
    name = fields.TextField()

    class Index:
        name = 'drug_types'

    class Django:
        model = DrugType


@registry.register_document
class INNDocument(Document):
    name = fields.TextField()

    class Index:
        name = 'inns'

    class Django:
        model = INN


@registry.register_document
class PrematureTerminationDocument(Document):
    date = fields.DateField()
    reason = fields.TextField()

    class Index:
        name = 'premature_terminations'

    class Django:
        model = PrematureTermination
