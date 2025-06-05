import zlib
import socket
import struct
import time
import random
from lxml import etree


def build_pricing_request():
    root = etree.Element("sirena")
    query = etree.SubElement(root, "query")
    pricing_route = etree.SubElement(query, "pricing_route")

    # Сегмент маршрута
    segment = etree.SubElement(pricing_route, "segment")
    etree.SubElement(segment, "departure").text = "МОВ"
    etree.SubElement(segment, "arrival").text = "СПТ"
    etree.SubElement(segment, "date").text = "03.06.25"
    etree.SubElement(segment, "company").text = "XX"
    etree.SubElement(segment, "class").text = "Э"

    ignore = etree.SubElement(segment, "ignore")

    acomp1 = etree.SubElement(ignore, "acomp", name="ZZ")
    etree.SubElement(acomp1, "flight").text = "*"

    acomp2 = etree.SubElement(ignore, "acomp", name="YY")
    etree.SubElement(acomp2, "flight").text = "433"
    etree.SubElement(acomp2, "flight").text = "433A"

    # Пассажир
    passenger = etree.SubElement(pricing_route, "passenger")
    etree.SubElement(passenger, "code").text = "ААА"
    etree.SubElement(passenger, "count").text = "1"

    # Параметры ответа
    answer_params = etree.SubElement(pricing_route, "answer_params")
    etree.SubElement(answer_params, "show_flighttime").text = "true"
    etree.SubElement(answer_params, "show_io_matching").text = "false"
    etree.SubElement(answer_params, "show_varianttotal").text = "true"
    etree.SubElement(answer_params, "show_available").text = "true"
    etree.SubElement(answer_params, "show_meals").text = "true"
    etree.SubElement(answer_params, "show_bag_norm_full").text = "true"

    request_params = etree.SubElement(pricing_route, "request_params")
    etree.SubElement(request_params, "min_results").text = "spOnePass"
    etree.SubElement(request_params, "max_results").text = "15"
    etree.SubElement(request_params, "timeout").text = "15"

    comb_rules = etree.SubElement(request_params, "comb_rules")

    rule1 = etree.SubElement(comb_rules, "rule", comb="no")
    etree.SubElement(rule1, "acomp").text = "*"

    rule2 = etree.SubElement(comb_rules, "rule", comb="yes")
    etree.SubElement(rule2, "acomp").text = "XX"
    etree.SubElement(rule2, "acomp").text = "YY"

    etree.SubElement(request_params, "formpay").text = "ПП"

    return etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)


def send_tcp_request(xml_data):
    compressed = zlib.compress(xml_data)

    msg_id = random.randint(10000, 99999)
    timestamp = int(time.time())
    cid = 5149  # Убедись, что это верный Client ID

    header = bytearray(100)
    struct.pack_into("!I", header, 0, len(compressed))     # длина тела
    struct.pack_into("!I", header, 4, timestamp)           # timestamp
    struct.pack_into("!I", header, 8, msg_id)              # message ID
    struct.pack_into("!H", header, 44, cid)                # client ID
    struct.pack_into("!B", header, 46, 0x04)               # флаг: zlib-сжатие

    payload = header + compressed

    with socket.create_connection(("193.104.87.251", 34323), timeout=10) as sock:
        sock.sendall(payload)
        response_header = sock.recv(100)
        resp_len = struct.unpack_from("!I", response_header)[0]

        if resp_len == 0:
            print("⚠️ Ответ имеет нулевую длину — проверь Client ID или XML-формат")

        resp_data = b""
        while len(resp_data) < resp_len:
            chunk = sock.recv(resp_len - len(resp_data))
            if not chunk:
                break
            resp_data += chunk

    return zlib.decompress(resp_data)


if __name__ == "__main__":
    xml_request = build_pricing_request()
    print("📤 Отправляем XML-запрос")

    try:
        xml_response = send_tcp_request(xml_request)
        print("✅ Ответ от сервера:\n", xml_response.decode("utf-8"))
    except Exception as e:
        print("❌ Ошибка при отправке запроса:", str(e))
