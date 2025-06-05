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
    

class ConnectedCitiesSerializer(serializers.Serializer):
    point = serializers.CharField(required=True)
    from_ = serializers.CharField(default='true')
    to_ = serializers.CharField(default='true')

    
class SegmentSerializer(serializers.Serializer):
    departure = serializers.CharField(max_length=3)
    arrival = serializers.CharField(max_length=3)
    date = serializers.DateField(input_formats=['%d.%m.%Y', '%d.%m.%y'],format='%d.%m.%y')
    company = serializers.CharField(max_length=2, required=False, allow_blank=True)
    class_code = serializers.CharField(max_length=1, required=False, allow_blank=True)


class PassengerSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=3, default='ADT')  
    count = serializers.IntegerField(default=1, min_value=1)

class PricingRouteRequestSerializer(serializers.Serializer):
    segments = SegmentSerializer(many=True)  
    passengers = PassengerSerializer(many=True, required=False, default=[{"code": "ADT", "count": 1}])
    currency = serializers.CharField(max_length=3, required=False)




class ScheduleRequestSerializer(serializers.Serializer):
    departure = serializers.CharField(max_length=3, required=False)
    arrival = serializers.CharField(max_length=3, required=False)
    company = serializers.CharField(max_length=3, required=False, allow_blank=True)
    date = serializers.DateField(format='%d.%m.%y', input_formats=['%d.%m.%y'], required=False)
    date2 = serializers.DateField(format='%d.%m.%y', input_formats=['%d.%m.%y'], required=False)
    time_from = serializers.CharField(max_length=4, required=False)
    time_till = serializers.CharField(max_length=4, required=False)
    carriers = serializers.ListField(
        child=serializers.CharField(max_length=3),
        required=False
    )
    direct = serializers.BooleanField(required=False)

    only_m2_joints = serializers.BooleanField(required=False)
    joint_type = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get('departure') and not data.get('arrival'):
            raise serializers.ValidationError("Необходимо указать хотя бы 'departure' или 'arrival'")
        return data
