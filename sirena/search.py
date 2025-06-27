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


from lxml import etree

def parse_tax_elements(price_elem):
    if price_elem is None:
        return []
    taxes = []
    for tax in price_elem.findall("tax"):
        taxes.append({
            "code": tax.get("code"),
            "owner": tax.get("owner"),
            "amount": tax.text
        })
    return taxes

def parse_bag_elements(bag_norm_elements, include_prohibited=False):
    result = []
    for bag_norm in bag_norm_elements:
        bag_info = {
            "passenger_id": bag_norm.get("passenger-id"),
            "segment_id": bag_norm.get("segment-id"),
            "company": bag_norm.findtext("company"),
            "value": bag_norm.findtext("value"),
            "type": bag_norm.findtext("type"),
            "allowed": [],
            "prohibited": []
        }
        for allowed in bag_norm.findall("allowed"):
            bag_info["allowed"].append({
                "number": allowed.get("number"),
                "rfisc": allowed.findtext("rfisc"),
                "text": allowed.findtext("text")
            })
        if include_prohibited:
            for prohibited in bag_norm.findall("prohibited"):
                bag_info["prohibited"].append({
                    "rfisc": prohibited.findtext("rfisc"),
                    "text": prohibited.findtext("text")
                })
        comment_elem = bag_norm.find("comment")
        if comment_elem is not None:
            bag_info["comment"] = comment_elem.text.strip()
        result.append(bag_info)
    return result

def parse_pricing_response(xml_bytes):
    root = etree.fromstring(xml_bytes)
    variants = root.xpath("//answer/pricing_route/variant")

    results = []
    for var in variants:
        price_elem = var.find("variant_total")

        flights = []
        for fl in var.findall("flight"):
            fl_price = fl.find("price")

            vat_elem = fl_price.find("vat") if fl_price is not None else None
            vat_info = {
                "fare": vat_elem.get("fare") if vat_elem is not None else None,
                "zz": vat_elem.get("zz") if vat_elem is not None else None,
            } if vat_elem is not None else None

            fare_elem = fl_price.find("fare") if fl_price is not None else None
            fare_info = {
                "remark": fare_elem.get("remark") if fare_elem is not None else None,
                "fare_expdate": fare_elem.get("fare_expdate") if fare_elem is not None else None,
                "code": fare_elem.get("code") if fare_elem is not None else None,
                "base_code": fare_elem.get("base_code") if fare_elem is not None else None,
                "amount": fare_elem.text if fare_elem is not None else None
            } if fare_elem is not None else None

            flights.append({
                "company": fl.findtext("company"),
                "num": fl.findtext("num"),
                "origin": {
                    "code": fl.findtext("origin"),
                    "terminal": fl.find("origin").get("terminal") if fl.find("origin") is not None else None,
                },
                "destination": {
                    "code": fl.findtext("destination"),
                    "terminal": fl.find("destination").get("terminal") if fl.find("destination") is not None else None,
                },
                "deptdate": {
                    "date": fl.findtext("deptdate"),
                    "delay": fl.find("deptdate").get("delay") if fl.find("deptdate") is not None else None,
                },
                "arrvdate": {
                    "date": fl.findtext("arrvdate"),
                    "delay": fl.find("arrvdate").get("delay") if fl.find("arrvdate") is not None else None,
                },
                "depttime": fl.findtext("depttime"),
                "arrvtime": fl.findtext("arrvtime"),
                "subclass": {
                    "cabin": fl.find("subclass").get("cabin") if fl.find("subclass") is not None else None,
                    "code": fl.findtext("subclass")
                },
                "meal": {
                    "subclass": fl.find("meal").get("subclass") if fl.find("meal") is not None else None,
                    "description": fl.find("meal").get("description") if fl.find("meal") is not None else None,
                    "code": fl.findtext("meal")
                },
                "flightTime": fl.findtext("flightTime"),
                "available": fl.findtext("available"),
                "airplane": fl.findtext("airplane"),
                "mileage": fl.findtext("mileage"),
                "price": {
                    "passenger_id": fl_price.get("passenger-id") if fl_price is not None else None,
                    "code": fl_price.get("code") if fl_price is not None else None,
                    "count": fl_price.get("count") if fl_price is not None else None,
                    "currency": fl_price.get("currency") if fl_price is not None else None,
                    "ticket": fl_price.get("ticket") if fl_price is not None else None,
                    "ticket_cpn": fl_price.get("ticket_cpn") if fl_price is not None else None,
                    "baggage": fl_price.get("baggage") if fl_price is not None else None,
                    "fc": fl_price.get("fc") if fl_price is not None else None,
                    "doc_type": fl_price.get("doc_type") if fl_price is not None else None,
                    "doc_id": fl_price.get("doc_id") if fl_price is not None else None,
                    "accode": fl_price.get("accode") if fl_price is not None else None,
                    "validating_company": fl_price.get("validating_company") if fl_price is not None else None,
                    "fop": fl_price.get("fop") if fl_price is not None else None,
                    "brand": fl_price.get("brand") if fl_price is not None else None,
                    "orig_code": fl_price.get("orig_code") if fl_price is not None else None,
                    "orig_id": fl_price.get("orig_id") if fl_price is not None else None,
                    "vat": vat_info,
                    "fare": fare_info,
                    "taxes": parse_tax_elements(fl_price),
                    "total": fl_price.findtext("total") if fl_price is not None else None
                }
            })

        # Собираем transfer times
        transfers = []
        for stt in var.findall("segmentTransferTime"):
            transfers.append({
                "segment_num": stt.get("iSegmentNum"),
                "segment_orig": stt.get("iSegmentOrig"),
                "segment_dest": stt.get("iSegmentDest"),
                "transfer_time": stt.text
            })

        results.append({
            "seance": var.get("seance"),
            "et_blanks": var.get("et_blanks"),
            "flights": flights,
            "segment_transfer_times": transfers,
            "total_price": price_elem.text if price_elem is not None else None,
            "currency": price_elem.get("currency") if price_elem is not None else None,
            "baggage_info": parse_bag_elements(var.findall(".//bag_norm_full/free_bag_norm"), include_prohibited=True),
            "carry_on_info": parse_bag_elements(var.findall(".//bag_norm_full/free_carry_on"))
        })

    return results
