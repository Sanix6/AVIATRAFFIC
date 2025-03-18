#restframework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

#apps
from .models import Banner, PopularDirection, Category
from .serializers import BannerSerializers, PopularDirectionSerializers, CategorySerializers


class BaseView(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='banners')
    def get_banners(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializers(banners, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='popular-directions')
    def get_popular_directions(self, request):
        popular_directions = PopularDirection.objects.all()
        serializer = PopularDirectionSerializers(popular_directions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='category')
    def get_category(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializers(queryset, many=True)
        return Response(serializer.data)