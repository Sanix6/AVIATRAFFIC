from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics, status, viewsets


#apps
from apps.avia.models import *
from apps.avia.serializers import *


class AviaParamsView(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='params')
    def get_city(self, request):
        queryset = Countries.objects.all()
        serilizer = CountrySerializer(queryset, many=True)
        return Response({'contiries': serilizer.data})