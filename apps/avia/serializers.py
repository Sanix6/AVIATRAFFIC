from rest_framework import serializers
from apps.avia.models import *


class AirportsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Airports
        fields = ['name', 'code_name']


class CitySerializer(serializers.ModelSerializer):
    aero = AirportsSerializers()
    class Meta:
        model = Cities
        fields = ['id','name', 'code_name', 'aero']

    def get_aero(self, obj):
        return AirportsSerializers(obj.aero).data


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer()
    class Meta:
        model = Countries
        fields = ['id','name', 'code_name', 'img','cities']


    def get_cities(self, obj):
        return CitySerializer(obj.country).data