# Drf package
from rest_framework import serializers
# Custom package
from api.models import District, ConfirmedCase


class ConfirmedCaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ConfirmedCase
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    confirmed_cases = ConfirmedCaseSerializer(many=True)

    class Meta:
        model = District
        fields = "__all__"
