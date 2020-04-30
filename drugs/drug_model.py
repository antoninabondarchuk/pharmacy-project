from django.db import models
from drugs.models import InternationalName, MarketingStatus, PharmacotherapeuticGroup, ATC, DrugType, \
    PrematureTermination, INN
from firms.models import UUIDClass, Applicant, Manufacturer


class Drug(UUIDClass):
    source_id = models.CharField(max_length=50, null=True)
    trade_name = models.TextField(null=True)
    international_name = models.ForeignKey(InternationalName, on_delete=models.CASCADE, null=True,
                                           related_name="international_names")
    drug_form = models.TextField()
    marketing_status = models.ForeignKey(MarketingStatus, on_delete=models.CASCADE, null=True,
                                         related_name="marketing_status_set")
    formula = models.TextField(null=True)
    pharmacotherapeutic_group = models.ForeignKey(PharmacotherapeuticGroup, on_delete=models.CASCADE, null=True)
    atcs = models.ManyToManyField(ATC, related_name="atcs_set")
    drug_applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=True)
    manufacturers = models.ManyToManyField(Manufacturer, related_name="manufacturers_set")
    registration_number = models.CharField(max_length=30, null=True)
    registration_date = models.DateField(null=True)
    expiration_date = models.CharField(max_length=20, null=True)
    drug_type = models.ForeignKey(DrugType, on_delete=models.CASCADE, null=True)
    has_bio_origin = models.BooleanField(null=True)
    has_phyto_origin = models.BooleanField(null=True)
    is_orphan = models.BooleanField(null=True)
    is_homeopatic = models.BooleanField(null=True)
    INN = models.ForeignKey(INN, on_delete=models.CASCADE, null=True)
    premature_termination = models.ForeignKey(PrematureTermination, on_delete=models.CASCADE, null=True)
    instruction_url = models.TextField(null=True)

    class Meta:
        ordering = ("trade_name", )

    def __str__(self):
        return f"Drug ({self.id}) (s_id:{self.source_id}) {self.trade_name}"

#
# def update_search(instance, **kwargs):
#     instance.to_search().save()
#
#
# post_save.connect(update_search, sender=Drug)
