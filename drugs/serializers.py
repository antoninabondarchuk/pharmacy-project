from rest_framework import serializers
from drugs.documents import DrugDocument
from drugs.drug_model import Drug
from drugs.models import ATC, MarketingStatus, InternationalName, PharmacotherapeuticGroup, DrugType, \
    PrematureTermination, INN
from firms.models import Country, Applicant, Manufacturer
from firms.serializers import ApplicantSerializer, ManufacturerSerializer


class AtcSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATC
        fields = (
            'name',
            'type',
        )


class MarketingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingStatus
        fields = (
            'name',
        )


class InternationalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalName
        fields = (
            'name',
        )


class PharmacotherapeuticGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacotherapeuticGroup
        fields = (
            'name',
        )


class DrugTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugType
        fields = (
            'name',
        )


class INNSerializer(serializers.ModelSerializer):
    class Meta:
        model = INN
        fields = (
            'name',
        )


class PrematureTerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrematureTermination
        fields = (
            'date',
            'reason',
        )


class DrugSerializer(serializers.ModelSerializer):

    international_name = InternationalNameSerializer()
    marketing_status = MarketingStatusSerializer(required=False)
    pharmacotherapeutic_group = PharmacotherapeuticGroupSerializer()
    atcs = AtcSerializer(many=True, required=False)
    drug_applicant = ApplicantSerializer()
    manufacturers = ManufacturerSerializer(many=True)
    drug_type = DrugTypeSerializer()
    INN = InternationalNameSerializer(required=False)
    premature_termination = PrematureTerminationSerializer(required=False)

    class Meta:
        document = DrugDocument
        model = Drug
        fields = (
            '__all__'
        )

    def create(self, validated_data):
        instance = Drug()
        instance.save()
        international_name = validated_data.get('international_name')
        international_name__name = international_name.get('name')
        instance.international_name, _ = InternationalName.objects.get_or_create(name=international_name__name)

        marketing_status = validated_data.get('marketing_status')
        marketing_status__name = marketing_status.get('name')
        instance.marketing_status, _ = MarketingStatus.objects.get_or_create(name=marketing_status__name)

        pharmacotherapeutic_group = validated_data.get('pharmacotherapeutic_group')
        pharmacotherapeutic_group__name = pharmacotherapeutic_group.get('name')
        instance.pharmacotherapeutic_group, _ = PharmacotherapeuticGroup.objects.get_or_create(
            name=pharmacotherapeutic_group__name)

        atcs = validated_data.get('atcs', [])
        for atc in atcs:
            new_atc, _ = ATC.objects.get_or_create(name=atc.get('name'), type=atc.get('type'))
            instance.atcs.add(new_atc)
            instance.save()

        drug_applicant = validated_data.get('drug_applicant')
        drug_applicant_address = drug_applicant.get('address')
        drug_applicant__country_id_name = drug_applicant.get('country_id').get('name')
        drug_applicant_name = drug_applicant.get('name')
        instance.drug_applicant, _ = Applicant.objects.get_or_create(name=drug_applicant_name,
                                                                     address=drug_applicant_address)
        instance.drug_applicant.country_id, _ = Country.objects.get_or_create(name=drug_applicant__country_id_name)

        manufacturers = validated_data.get('manufacturers', [])
        for manufacturer in manufacturers:
            manufacturer_name = manufacturer.get('name')
            manufacturer_address = manufacturer.get('address')
            manufacturer_country_id__name = manufacturer.get('country_id').get('name')
            new_manufacturer, _ = Manufacturer.objects.get_or_create(name=manufacturer_name,
                                                                     address=manufacturer_address)
            new_manufacturer.country_id, _ = Country.objects.get_or_create(name=manufacturer_country_id__name)
            instance.manufacturers.add(new_manufacturer)
            instance.save()

        drug_type = validated_data.get('drug_type')
        drug_type__name = drug_type.get('name')
        instance.drug_type, _ = DrugType.objects.get_or_create(name=drug_type__name)

        inn_dict = validated_data.get('INN')
        inn_name = inn_dict.get('name')
        instance.INN, _ = INN.objects.get_or_create(name=inn_name)

        premature_termination = validated_data.get('premature_termination')
        premature_termination__date = premature_termination.get('date')
        premature_termination__reason = premature_termination.get('reason')
        instance.premature_termination, _ = PrematureTermination.objects.get_or_create(
            date=premature_termination__date, reason=premature_termination__reason)

        instance.source_id = validated_data.get('source_id')
        instance.trade_name = validated_data.get('trade_name')
        instance.expiration_date = validated_data.get('expiration_date')
        instance.formula = validated_data.get('formula')
        instance.has_bio_origin = validated_data.get('has_bio_origin')
        instance.has_phyto_origin = validated_data.get('has_phyto_origin')
        instance.instruction_url = validated_data.get('instruction_url')
        instance.is_homeopatic = validated_data.get('is_homeopatic')
        instance.is_orphan = validated_data.get('is_orphan')
        instance.registration_date = validated_data.get('registration_date')
        instance.registration_number = validated_data.get('registration_number')
        instance.drug_form = validated_data.get('drug_form')

        instance.save()
        return instance
