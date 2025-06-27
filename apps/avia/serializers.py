from rest_framework import serializers
from apps.avia.models import *
from rest_framework import serializers

class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = [
            "company", "flight", "departure", "arrival",
            "date", "subclass", "joint_id"
        ]


class PassengerSerializer(serializers.ModelSerializer):
    birthdate = serializers.CharField()

    class Meta:
        model = Passenger
        fields = [
            "lastname", "firstname", "surname",
            "category", "sex", "birthdate",
            "doc_country", "doccode", "doc"
        ]


class BookingRequestSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True)
    passengers = PassengerSerializer(many=True)
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Booking
        fields = ["segments", "passengers", "phone", "email"]



class RaceInfoSerializer(serializers.Serializer):
    company = serializers.CharField(max_length=2)
    flight = serializers.CharField(max_length=10)
    date = serializers.DateField(required=False, input_formats=["%d.%m.%y", "%Y-%m-%d"])
    show_flighttime = serializers.BooleanField(required=False, default=False)
    show_baseclass = serializers.BooleanField(required=False, default=False)

    def to_internal_value(self, data):
        answer_params = data.pop("answer_params", {})
        data.update(answer_params)
        return super().to_internal_value(data)
    
class SearchSegmentsSerializer(serializers.Serializer):
    departure = serializers.CharField(max_length=3)
    arrival = serializers.CharField(max_length=3)
    date= serializers.DateField(format="%d.%m.%y", input_formats=["%d.%m.%y"])


class SearchPassengerSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=3)
    count = serializers.IntegerField(min_value=1)

class PricingRouteSerializer(serializers.Serializer):
    segments = SearchSegmentsSerializer(many=True)
    passengers = SearchPassengerSerializer(many=True)
    currency = serializers.CharField(max_length=3)

class BookingINFOSerializer(serializers.Serializer):
    surname = serializers.CharField()
    regnum = serializers.CharField()
