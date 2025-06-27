from lxml import etree
from datetime import date, datetime


def format_date(raw_date):
    return raw_date.strftime("%d.%m.%y") if isinstance(raw_date, (datetime, date)) else raw_date


def build_raceinfo_request(data: dict) -> bytes:
    """XML-запрос для получения информации о рейсе (raceinfo)."""
    root = etree.Element("sirena")
    query = etree.SubElement(root, "query")
    raceinfo = etree.SubElement(query, "raceinfo")

    etree.SubElement(raceinfo, "company").text = data["company"]
    etree.SubElement(raceinfo, "flight").text = data["flight"]

    if data.get("date"):
        etree.SubElement(raceinfo, "date").text = format_date(data["date"])

    if "answer_params" in data:
        answer_params = etree.SubElement(raceinfo, "answer_params")
        for key, value in data["answer_params"].items():
            etree.SubElement(answer_params, key).text = "true" if value else "false"

    return etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True)


def parse_segment_element(segment_elem):
    """Парсинг ответа блока Segments"""
    return {
        "departure": segment_elem.findtext("departure"),
        "departure_port": segment_elem.find("departure").get("port") if segment_elem.find("departure") is not None else None,
        "arrival": segment_elem.findtext("arrival"),
        "arrival_port": segment_elem.find("arrival").get("port") if segment_elem.find("arrival") is not None else None,
        "depttime": segment_elem.findtext("depttime"),
        "arrvtime": segment_elem.findtext("arrvtime"),
        "status": segment_elem.findtext("status"),
        "flight_time": segment_elem.findtext("flightTime")
    }


def parse_raceinfo_response(xml_bytes):
    """Парсинг полного ответа raceinfo"""
    root = etree.fromstring(xml_bytes)
    raceinfo_elem = root.find(".//raceinfo")

    response_info = {
        "company": raceinfo_elem.findtext("company") if raceinfo_elem is not None else None,
        "num": raceinfo_elem.findtext("num") if raceinfo_elem is not None else None,
        "date": raceinfo_elem.findtext("date") if raceinfo_elem is not None else None,
        "navigation": []
    }

    for nav in root.findall(".//navigation"):
        navigation = {
            "airplane": nav.findtext("airplane"),
            "date_beg": nav.findtext("date_beg"),
            "date_end": nav.findtext("date_end"),
            "subclasses": [subcls.text for subcls in nav.findall("subclass")],
            "segments": [parse_segment_element(seg) for seg in nav.findall("segment")]
        }
        response_info["navigation"].append(navigation)

    return response_info


def build_order_request(data: dict) -> bytes:
    """Используется для получения информации о созданном ранее PNR."""
    root = etree.Element("sirena")
    query = etree.SubElement(root, "query")  
    order = etree.SubElement(query, "order")  

    etree.SubElement(order, "surname").text = data["surname"]
    etree.SubElement(order, "regnum").text = data["regnum"]

    if "answer_params" in data:
        answer_params = etree.SubElement(order, "answer_params")
        for key, value in data["answer_params"].items():
            etree.SubElement(answer_params, key).text = "true" if value else "false"
    return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)


def parse_order_response(xml_bytes: bytes) -> dict:
    result = {
        "agency": None,
        "pnr": {
            "bdate": None,
            "passengers": [],
            "segments": [],
            "prices": [],
            "variant_total": None,
            "regnum": None,
            "version": None,
            "common_status": None,
            "possible_actions": [],
        },
        "contacts": [],
        "remarks": [],
        "special_services": [],
        "latin_registration": False,
        "tickinfo": {}
    }

    root = etree.fromstring(xml_bytes)

    order = root.find(".//order")
    if order is not None:
        result["agency"] = order.attrib.get("agency")

        # PNR
        pnr = order.find("pnr")
        if pnr is not None:
            result["pnr"]["bdate"] = pnr.attrib.get("bdate")

            # Passengers
            for p in pnr.findall(".//passenger"):
                result["pnr"]["passengers"].append({
                    "id": p.attrib.get("id"),
                    "lead_pass": p.attrib.get("lead_pass") == "true",
                    "name": p.findtext("name"),
                    "surname": p.findtext("surname"),
                    "sex": p.findtext("sex"),
                    "birthdate": p.findtext("birthdate"),
                    "age": p.findtext("age"),
                    "doccode": p.findtext("doccode"),
                    "doc": p.findtext("doc"),
                    "pspexpire": p.findtext("pspexpire"),
                    "category": p.findtext("category"),
                    "n_seats": p.findtext("n_seats"),
                    "doc_country": p.findtext("doc_country"),
                    "nationality": p.findtext("nationality"),
                    "residence": p.findtext("residence")
                })

            # Segments
            for s in pnr.findall(".//segment"):
                result["pnr"]["segments"].append({
                    "id": s.attrib.get("id"),
                    "company": s.findtext("company"),
                    "flight": s.findtext("flight"),
                    "class": s.findtext("class"),
                    "seatcount": s.findtext("seatcount"),
                    "airplane": s.findtext("airplane"),
                    "departure": {
                        "city": s.findtext("departure/city"),
                        "airport": s.findtext("departure/airport"),
                        "date": s.findtext("departure/date"),
                        "time": s.findtext("departure/time")
                    },
                    "arrival": {
                        "city": s.findtext("arrival/city"),
                        "airport": s.findtext("arrival/airport"),
                        "date": s.findtext("arrival/date"),
                        "time": s.findtext("arrival/time")
                    },
                    "status": s.find("status").attrib.get("text") if s.find("status") is not None else None,
                    "flightTime": s.findtext("flightTime"),
                    "remote_recloc": s.findtext("remote_recloc"),
                    "cabin": s.findtext("cabin"),
                    "booking_cabin": s.findtext("booking_cabin")
                })

            # Prices
            prices = pnr.find("prices")
            if prices is not None:
                for pr in prices.findall("price"):
                    fare = pr.find("fare")
                    fare_data = {
                        "remark": fare.attrib.get("remark") if fare is not None else None,
                        "fare_expdate": fare.attrib.get("fare_expdate") if fare is not None else None,
                        "value": fare.findtext("value"),
                        "currency": fare.find("value").attrib.get("currency") if fare.find("value") is not None else None,
                        "code": fare.findtext("code")
                    } if fare is not None else {}

                    taxes = []
                    for tax in pr.findall(".//tax"):
                        taxes.append({
                            "code": tax.findtext("code"),
                            "value": tax.findtext("value"),
                            "currency": tax.attrib.get("currency", tax.find("value").attrib.get("currency") if tax.find("value") is not None else None)
                        })

                    result["pnr"]["prices"].append({
                        "segment_id": pr.attrib.get("segment-id"),
                        "passenger_id": pr.attrib.get("passenger-id"),
                        "code": pr.attrib.get("code"),
                        "ticket": pr.attrib.get("ticket"),
                        "fare": fare_data,
                        "taxes": taxes,
                        "total": pr.findtext("total"),
                        "currency": pr.attrib.get("currency")
                    })

                result["pnr"]["variant_total"] = prices.findtext("variant_total")

            result["pnr"]["regnum"] = pnr.findtext("regnum")
            result["pnr"]["version"] = pnr.findtext("version")
            result["pnr"]["common_status"] = pnr.findtext("common_status")

            for act in pnr.findall(".//possible_action_list/action"):
                result["pnr"]["possible_actions"].append(act.text)

        # Contacts
        for email in order.findall(".//email"):
            result["contacts"].append({
                "type": "email",
                "value": email.text,
                "cont_id": email.attrib.get("cont_id"),
                "loc_id": email.attrib.get("loc_id")
            })
        for phone in order.findall(".//contact"):
            result["contacts"].append({
                "type": phone.attrib.get("type"),
                "value": phone.text,
                "comment": phone.attrib.get("comment"),
                "cont_id": phone.attrib.get("cont_id"),
                "loc_id": phone.attrib.get("loc_id")
            })

        # Remarks
        for rem in order.findall(".//remark"):
            result["remarks"].append({
                "rem_id": rem.attrib.get("rem_id"),
                "carrier": rem.attrib.get("carrier"),
                "pass_id": rem.attrib.get("pass_id"),
                "text": rem.text
            })

        # Special services
        for ssr in order.findall(".//ssr"):
            result["special_services"].append({
                "type": ssr.attrib.get("type"),
                "text": ssr.attrib.get("text"),
                "confirmed": ssr.attrib.get("confirmed") == "yes",
                "status": ssr.attrib.get("status"),
                "key": ssr.attrib.get("key")
            })

        result["latin_registration"] = order.findtext("latin_registration") == "true"

        # Tickinfo
        tickinfo = order.find("tickinfo")
        if tickinfo is not None:
            result["tickinfo"] = {
                "ticknum": tickinfo.attrib.get("ticknum"),
                "tick_ser": tickinfo.attrib.get("tick_ser"),
                "is_etick": tickinfo.attrib.get("is_etick") == "true",
                "accode": tickinfo.attrib.get("accode"),
                "tkt_ppr": tickinfo.attrib.get("tkt_ppr"),
                "print_time": tickinfo.attrib.get("print_time"),
                "can_void": tickinfo.attrib.get("can_void") == "true",
                "void_timelimit_utc": tickinfo.attrib.get("void_timelimit_utc"),
                "seg_id": tickinfo.attrib.get("seg_id"),
                "pass_id": tickinfo.attrib.get("pass_id"),
                "ticket_cpn": tickinfo.attrib.get("ticket_cpn"),
                "involuntary_refund_available": tickinfo.attrib.get("involuntary_refund_available") == "true",
                "agency": tickinfo.attrib.get("agency"),
                "status": tickinfo.text
            }

    return result