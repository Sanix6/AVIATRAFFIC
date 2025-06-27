from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from apps.avia.models import Countries
from apps.avia import serializers

from sirena import client, search, city, offers, booking


class SearchTicketView(generics.GenericAPIView):
    serializer_class = serializers.PricingRouteSerializer

    @swagger_auto_schema(
        operation_description="Поиск авиабилетов",
        request_body=serializers.PricingRouteSerializer,
        responses={200: "Успешный ответ с вариантами перевозки"}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        xml_request = search.build_pricing_route_request(validated_data)
        xml_response = client.send_tcp_request(xml_request)
        result = search.parse_pricing_response(xml_response)

        if not result:
            return Response({
                "response_xml": xml_response.decode('utf-8')
            }, status=status.HTTP_200_OK)

        return Response(result, status=status.HTTP_200_OK)



class RaceInfoView(generics.GenericAPIView):
    serializer_class = serializers.RaceInfoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        request_xml = offers.build_raceinfo_request({
            "company": validated["company"],
            "flight": validated["flight"],
            "date": validated.get("date"),
            "answer_params": {
                "show_flighttime": validated.get("show_flighttime", False),
                "show_baseclass": validated.get("show_baseclass", False),
            }
        })

        try:
            response_xml = client.send_tcp_request(request_xml)
            response_data = offers.parse_raceinfo_response(response_xml)
            return Response(response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
class BookingView(generics.GenericAPIView):
    serializer_class = serializers.BookingRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking_data = serializer.validated_data

        try:
            xml_str = booking.build_booking_xml(booking_data)
            raw_xml = xml_str.encode('utf-8')
            xml_response_bytes = client.send_tcp_request(raw_xml)
            xml_response = xml_response_bytes.decode('utf-8')
            result = booking.parse_booking_response(xml_response)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Получить детали бронирования по фамилии и номеру брони",
        request_body=serializers.OrderRequestSerializer,
        responses={200: openapi.Response("Информация о брони", serializers.OrderRequestSerializer)}
    )
    def post(self, request):
        serializer = serializers.OrderRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        surname = serializer.validated_data["surname"]
        regnum = serializer.validated_data["regnum"]

        xml_request = offers.build_order_request({
            "surname": surname,
            "regnum": regnum
        })

        try:
            xml_response_bytes = client.send_tcp_request(xml_request)
            parsed_data = offers.parse_order_response(xml_response_bytes)
            return Response(parsed_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class BookingCancelView(generics.GenericAPIView):
    serializer_class = serializers.BookingINFOSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        xml_request = booking.build_booking_cancel(serializer.validated_data)
        try:
            xml_response = client.send_tcp_request(xml_request)
            success = booking.parse_booking_cancel_response(xml_response)
            if success:
                return Response({"detail": "Бронирование отменено успешно"})
            return Response({"detail": "Не удалось отменить бронирование"}, status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)