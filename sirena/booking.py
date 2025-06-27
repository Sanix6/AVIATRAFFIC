from lxml import etree

def safe_text(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()
    return str(value)

def build_booking_xml(data: dict) -> str:
    sirena = etree.Element("sirena")
    query = etree.SubElement(sirena, "query")
    booking = etree.SubElement(query, "booking")

    for seg in data.get("segments", []):
        segment = etree.SubElement(booking, "segment")
        etree.SubElement(segment, "company").text = safe_text(seg.get("company"))
        etree.SubElement(segment, "flight").text = safe_text(seg.get("flight"))
        etree.SubElement(segment, "departure").text = safe_text(seg.get("departure"))
        etree.SubElement(segment, "arrival").text = safe_text(seg.get("arrival"))
        etree.SubElement(segment, "date").text = safe_text(seg.get("date"))
        etree.SubElement(segment, "subclass").text = safe_text(seg.get("subclass"))

    for pax in data.get("passengers", []):
        passenger = etree.SubElement(booking, "passenger")
        etree.SubElement(passenger, "lastname").text = safe_text(pax.get("lastname"))

        firstname = pax.get("firstname", "")
        surname = pax.get("surname", "")
        full_firstname = f"{firstname} {surname}".strip()
        etree.SubElement(passenger, "firstname").text = safe_text(full_firstname)

        if pax.get("birthdate"):
            etree.SubElement(passenger, "birthdate").text = safe_text(pax.get("birthdate"))
        if pax.get("sex"):
            etree.SubElement(passenger, "sex").text = safe_text(pax.get("sex"))
        if pax.get("category"):
            etree.SubElement(passenger, "category").text = safe_text(pax.get("category"))
        if pax.get("doccode"):
            etree.SubElement(passenger, "doccode").text = safe_text(pax.get("doccode"))
        if pax.get("doc"):
            etree.SubElement(passenger, "doc").text = safe_text(pax.get("doc"))
        if pax.get("doc_country"):
            etree.SubElement(passenger, "doc_country").text = safe_text(pax.get("doc_country"))
        if pax.get("nationality"):
            etree.SubElement(passenger, "nationality").text = safe_text(pax.get("nationality"))
        if pax.get("residence"):
            etree.SubElement(passenger, "residence").text = safe_text(pax.get("residence"))

    phone_value = data.get("phone")
    email_value = data.get("email")
    customer_data = data.get("customer", {})

    phone_value = phone_value or customer_data.get("phone")
    email_value = email_value or customer_data.get("email")

    if phone_value or email_value:
        customer = etree.SubElement(booking, "customer")
        if phone_value:
            etree.SubElement(customer, "phone", type="mobile").text = safe_text(phone_value)
        if email_value:
            etree.SubElement(customer, "email").text = safe_text(email_value)

    answer_params = etree.SubElement(booking, "answer_params")
    etree.SubElement(answer_params, "add_remote_recloc").text = "true"

    xml_bytes = etree.tostring(
        sirena,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8"
    )
    return xml_bytes.decode("utf-8")

def parse_booking_response(xml_str: str) -> dict:
    result = {
        "status": "unknown",
        "regnum": None,
        "pnr": None,
        "errors": [],
        "raw_response": xml_str, 
    }

    try:
        root = etree.fromstring(xml_str.encode("utf-8"))

        booking_el = root.find(".//booking")
        if booking_el is None:
            error_els = root.findall(".//error")
            if error_els:
                for e in error_els:
                    if e.text:
                        result["errors"].append(e.text)
                result["status"] = "error"
            else:
                result["status"] = "error"
                result["errors"].append("No booking element found in response")
            return result

        regnum = booking_el.get("regnum")
        if regnum:
            result["regnum"] = regnum

        pnr_el = booking_el.find("pnr")
        if pnr_el is not None:
            pnr_data = {
                "passengers": [],
                "segments": [],
                "prices": [],
                "timelimit": None,
            }

            for pax_el in pnr_el.findall(".//passenger"):
                pax = {
                    "id": pax_el.get("id"),
                    "lead_pass": pax_el.get("lead_pass"),
                    "name": pax_el.findtext("name"),
                    "surname": pax_el.findtext("surname"),
                    "sex": pax_el.findtext("sex"),
                    "birthdate": pax_el.findtext("birthdate"),
                    "age": pax_el.findtext("age"),
                    "doccode": pax_el.findtext("doccode"),
                    "doc": pax_el.findtext("doc"),
                    "pspexpire": pax_el.findtext("pspexpire"),
                    "category": pax_el.findtext("category"),
                    "n_seats": pax_el.findtext("n_seats"),
                    "doc_country": pax_el.findtext("doc_country"),
                    "nationality": pax_el.findtext("nationality"),
                    "residence": pax_el.findtext("residence"),
                }
                pnr_data["passengers"].append(pax)

            for seg_el in pnr_el.findall(".//segment"):
                seg = {
                    "id": seg_el.get("id"),
                    "company": seg_el.findtext("company"),
                    "flight": seg_el.findtext("flight"),
                    "subclass": seg_el.findtext("subclass"),
                    "status_text": seg_el.find("status").get("text") if seg_el.find("status") is not None else None,
                    "status": seg_el.findtext("status"),
                    "departure_city": seg_el.findtext("departure/city"),
                    "departure_airport": seg_el.findtext("departure/airport"),
                    "departure_date": seg_el.findtext("departure/date"),
                    "departure_time": seg_el.findtext("departure/time"),
                    "arrival_city": seg_el.findtext("arrival/city"),
                    "arrival_airport": seg_el.findtext("arrival/airport"),
                    "arrival_date": seg_el.findtext("arrival/date"),
                    "arrival_time": seg_el.findtext("arrival/time"),
                    "flightTime": seg_el.findtext("flightTime"),
                }
                pnr_data["segments"].append(seg)

            prices_el = pnr_el.find("prices")
            if prices_el is not None:
                prices = []
                for price_el in prices_el.findall("price"):
                    price = {
                        "segment_id": price_el.get("segment-id"),
                        "passenger_id": price_el.get("passenger-id"),
                        "code": price_el.get("code"),
                        "count": price_el.get("count"),
                        "currency": price_el.get("currency"),
                        "ticket": price_el.get("ticket"),
                        "total": price_el.findtext("total") or price_el.findtext(".//value"),
                    }
                    prices.append(price)
                pnr_data["prices"] = prices

            timelimit = pnr_el.findtext("timelimit")
            if timelimit:
                pnr_data["timelimit"] = timelimit

            result["pnr"] = pnr_data
            result["status"] = "success"
        else:
            result["status"] = "error"
            result["errors"].append("PNR element missing in booking")

    except Exception as e:
        result["status"] = "error"
        result["errors"].append(str(e))

    return result



def build_booking_cancel(data: dict) -> bytes:
    """Используется для отмены бронирование"""
    root = etree.Element("sirena")
    query = etree.SubElement(root, "query")  
    bookingcancel = etree.SubElement(query, "booking-cancel")  

    etree.SubElement(bookingcancel, "regnum").text = data["regnum"]
    etree.SubElement(bookingcancel, "surname").text = data["surname"]
    return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)


def parse_booking_cancel_response(xml_response: bytes) -> bool:
    root = etree.fromstring(xml_response)
    return root.find(".//booking-cancel/ok") is not None