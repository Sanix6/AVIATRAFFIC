#restframework
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#apps
from .models import Banner, PopularDirection, Information, FAQ
from .serializers import BannerSerializers, PopularDirectionSerializers, InformationSerializers, SubInfoSerializer, FAQSerializer, FAQAnswersSerializers


class BaseView(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='banners')
    def get_banners(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializers(banners, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='popular-directions')
    def get_popular_directions(self, request):
        popular_directions = PopularDirection.objects.all()
        serializer = PopularDirectionSerializers(popular_directions, many=True, context={'request': request})
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='info')
    def get_information(self, request):
        queryset = Information.objects.all()
        serializer = InformationSerializers(queryset, many=True, context={'request': request})
        return Response({'information': serializer.data})

    @swagger_auto_schema(
        operation_description="Получить список подкатегорий по slug",
        manual_parameters=[
            openapi.Parameter(
                'slug',
                openapi.IN_QUERY,
                description="Параметр для получение информации",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: SubInfoSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='sub-info')
    def get_subinfo(self, request):
        slug = request.query_params.get('slug')
        try:
            info = Information.objects.get(slug=slug)
        except Information.DoesNotExist:
            return Response({'error': 'Information not found'}, status=404)

        subcategories = info.subinfo.all()
        serializer = SubInfoSerializer(subcategories, many=True, context={'request': request})
        return Response(serializer.data)



class FAQListAPIView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class FAQDetailAPIView(generics.GenericAPIView):
    serializer_class = FAQAnswersSerializers

    def get(self, request, slug):
        try:
            faq = FAQ.objects.get(slug=slug)
            serializer = self.get_serializer(faq)
            return Response(serializer.data)
        except FAQ.DoesNotExist:
            return Response({'detail': 'FAQ not found'}, status=status.HTTP_404_NOT_FOUND)