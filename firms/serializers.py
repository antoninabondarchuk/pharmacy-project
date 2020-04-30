from rest_framework import serializers
from firms.models import Manufacturer, Country, Applicant


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = (
            'name',
        )


class ManufacturerSerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()

    class Meta:
        model = Manufacturer
        fields = (
            'name',
            'address',
            'country_id',
        )


class ApplicantSerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()

    class Meta:
        model = Applicant
        fields = (
            'name',
            'address',
            'country_id',
        )
