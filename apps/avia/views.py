from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
import xml.etree.ElementTree as ET
from apps.avia.models import *
from apps.avia.serializers import *
from sirena.client import *
from sirena.search import *
from sirena.settings import *
from sirena.city import *

class AviaParamsView(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='params')
    def get_city(self, request):
        queryset = Countries.objects.all()
        serilizer = CountrySerializer(queryset, many=True)
        return Response({'contiries': serilizer.data})



class SearchTicketView(generics.GenericAPIView):
    serializer_class = PricingRouteRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        xml_request = build_pricing_route_request(validated_data)
        xml_response = send_tcp_request(xml_request)
        result = parse_pricing_response(xml_response)

        if not result:
            return Response({
                "response_xml": xml_response.decode('utf-8')
            }, status=status.HTTP_200_OK)

        return Response(result, status=status.HTTP_200_OK)
    

class ConnectedCitiesView(generics.GenericAPIView):
    serializer_class = ConnectedCitiesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        xml_data = get_connected_cities(
            "instance_name", {
            'point': data['point'],
            'from': data['from_'],
            'to': data['to_'],})
        response_bytes = send_tcp_request(xml_data)
        result = pars_connected_cities(response_bytes)
        return Response(result, status=status.HTTP_200_OK)
           

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lxml import etree
import zlib
import socket
import struct
import time

class SirenaAvailabilityView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        if "availability" not in data:
            return Response({"error": "Missing 'availability' key"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            xml_data = self.build_request_xml(data)
            raw_response = self.send_tcp_request(xml_data)
            parsed_response = self.parse_response_xml(raw_response)
            return Response(parsed_response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def build_request_xml(self, data):
        root = etree.Element("sirena")
        query = etree.SubElement(root, "query")

        for avail in data["availability"]:
            availability = etree.SubElement(query, "availability")
            for key, value in avail.items():
                if key == "subclass":
                    for subclass in value:
                        etree.SubElement(availability, "subclass").text = subclass
                elif key == "request_params":
                    request_params = etree.SubElement(availability, "request_params")
                    for param_key, param_value in value.items():
                        etree.SubElement(request_params, param_key).text = param_value
                else:
                    etree.SubElement(availability, key).text = value

        return etree.tostring(root, encoding='utf-8', xml_declaration=True)

    def send_tcp_request(self, xml_data):
        compressed = zlib.compress(xml_data)
        msg_id = 12345
        timestamp = int(time.time())
        cid = 5149

        header = bytearray(100)
        struct.pack_into("!I", header, 0, len(compressed))
        struct.pack_into("!I", header, 4, timestamp)
        struct.pack_into("!I", header, 8, msg_id)
        struct.pack_into("!H", header, 44, cid)
        struct.pack_into("!B", header, 46, 0x04)

        payload = header + compressed

        with socket.create_connection(("193.104.87.251", 34323), timeout=10) as sock:
            sock.sendall(payload)
            response_header = sock.recv(100)
            resp_len = struct.unpack_from("!I", response_header)[0]
            resp_data = b""
            while len(resp_data) < resp_len:
                resp_data += sock.recv(resp_len - len(resp_data))

        return zlib.decompress(resp_data)

    def parse_response_xml(self, xml_bytes):
        root = etree.fromstring(xml_bytes)
        results = []

        for availability in root.xpath("//answer/availability"):
            flights = []
            for flight in availability.findall("flight"):
                flight_info = {
                    "company": flight.findtext("company"),
                    "num": flight.findtext("num"),
                    "origin": flight.findtext("origin"),
                    "destination": flight.findtext("destination"),
                    "depttime": flight.findtext("depttime"),
                    "arrvtime": flight.findtext("arrvtime"),
                    "airplane": flight.findtext("airplane"),
                    "service_type": flight.findtext("service_type"),
                    "subclasses": []
                }
                for subclass in flight.findall("subclass"):
                    flight_info["subclasses"].append({
                        "code": subclass.text,
                        "count": subclass.get("count")
                    })
                flights.append(flight_info)

            results.append({
                "departure": availability.get("departure"),
                "arrival": availability.get("arrival"),
                "flights": flights
            })

        return results
