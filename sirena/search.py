from lxml import etree
from sirena.settings import SIRENA_HOST, SIRENA_PORT
from sirena.client import send_xml_to_sirena

def build_availability_request(departure, arrival, date=None):
    root = etree.Element("sirena")
    query = etree.SubElement(root, "query")
    availability = etree.SubElement(query, "availability")

    etree.SubElement(availability, "departure").text = departure
    etree.SubElement(availability, "arrival").text = arrival

    if date:
        etree.SubElement(availability, "date").text = date

    req_params = etree.SubElement(availability, "request_params")
    etree.SubElement(req_params, "joint_type").text = "jtAll"

    return etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True)



def parse_availability_response(xml_data):
    tree = etree.fromstring(xml_data)
    flights = []
    
    for flight in tree.xpath("//flight"):
        flights.append({
            "company": flight.findtext("company"),
            "num": flight.findtext("num"),
            "origin": flight.findtext("origin"),
            "destination": flight.findtext("destination"),
            "depttime": flight.findtext("depttime"),
            "arrvtime": flight.findtext("arrvtime"),
            "airplane": flight.findtext("airplane"),
            "subclasses": [
                {
                    "code": sc.text,
                    "count": sc.attrib.get("count")
                } for sc in flight.findall("subclass")
            ],
        })

    return {"flights": flights}

def search_flights(from_code, to_code, date):
    xml_request = build_availability_request(from_code, to_code, date)
    xml_response = send_xml_to_sirena(xml_request, SIRENA_HOST, SIRENA_PORT)
    return parse_availability_response(xml_response)