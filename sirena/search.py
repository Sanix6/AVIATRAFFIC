from datetime import datetime, date
from lxml import etree


def format_date(raw_date):
    return raw_date.strftime("%d.%m.%y") if isinstance(raw_date, (datetime, date)) else raw_date

def build_segment_element(pricing, seg):
    segment = etree.SubElement(pricing, "segment")
    etree.SubElement(segment, "departure").text = seg["departure"]
    etree.SubElement(segment, "arrival").text = seg["arrival"]
    etree.SubElement(segment, "date").text = format_date(seg["date"])


def build_passenger_element(pricing, pax):
    passenger = etree.SubElement(pricing, "passenger")
    etree.SubElement(passenger, "code").text = pax.get("code", "ADT")
    etree.SubElement(passenger, "count").text = str(pax.get("count", 1))


def build_pricing_route_request(data):
    root = etree.Element("sirena")
    pricing = etree.SubElement(etree.SubElement(root, "query"), "pricing_route")

    for seg in data["segments"]:
        build_segment_element(pricing, seg)

    for pax in data["passengers"]:
        build_passenger_element(pricing, pax)

    etree.SubElement(pricing, "currency").text = data["currency"]

    return etree.tostring(root, encoding="utf-8", xml_declaration=True)



def parse_tax_elements(price_elem):
    return [
        {"code": tax.get("code"), "amount": tax.text}
        for tax in price_elem.findall("tax")
    ] if price_elem is not None else []


def parse_bag_elements(elements):
    result = []
    for bag in elements:
        entry = {
            "company": bag.findtext("company"),
            "value": bag.findtext("value"),
            "type": bag.findtext("type")
        }
        result.append(entry)
    return result


def parse_pricing_response(xml_bytes):
    root = etree.fromstring(xml_bytes)
    variants = root.xpath("//answer/pricing_route/variant")

    results = []
    for var in variants:
        price_elem = var.find("variant_total")
        flights = []
        for fl in var.findall("flight"):
            fl_price = fl.find(".//price")
            flights.append({
                "company": fl.findtext("company"),
                "num": fl.findtext("num"),
                "origin": fl.findtext("origin"),
                "destination": fl.findtext("destination"),
                "depttime": fl.findtext("depttime"),
                "arrvtime": fl.findtext("arrvtime"),
                "classes": [cls.text for cls in fl.findall("class")],
                "available": fl.findtext("available"),
                "airplane": fl.findtext("airplane"),
                "mileage": fl.findtext("mileage"),
                "subclass": fl.findtext("subclass"),
                "meal": fl.findtext("meal"),
                "price": {
                    "total": fl_price.findtext("total") if fl_price is not None else None,
                    "currency": fl_price.get("currency") if fl_price is not None else None,
                    "fare": fl_price.findtext("fare") if fl_price is not None else None,
                    "taxes": parse_tax_elements(fl_price)
                }
            })

        results.append({
            "flights": flights,
            "total_price": price_elem.text if price_elem is not None else None,
            "currency": price_elem.get("currency") if price_elem is not None else None,
            "baggage_info": parse_bag_elements(var.findall(".//bag_norm_full/free_bag_norm"), include_prohibited=True),
            "carry_on_info": parse_bag_elements(var.findall(".//bag_norm_full/free_carry_on"))
        })

    return results
