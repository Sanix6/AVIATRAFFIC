import zlib
import socket
import struct
import time

def send_tcp_request(xml_data):
    compressed = zlib.compress(xml_data.encode("utf-8"))
    msg_id = 12345
    timestamp = int(time.time())
    cid = 5149

    header = bytearray(100)
    struct.pack_into("!I", header, 0, len(compressed))     # Length of compressed data
    struct.pack_into("!I", header, 4, timestamp)           # Timestamp
    struct.pack_into("!I", header, 8, msg_id)              # Message ID
    struct.pack_into("!H", header, 44, cid)                # Client ID
    struct.pack_into("!B", header, 46, 0x04)               # Protocol version or flag

    payload = header + compressed

    with socket.create_connection(("193.104.87.251", 34323), timeout=10) as sock:
        sock.sendall(payload)

        response_header = sock.recv(100)
        resp_len = struct.unpack_from("!I", response_header)[0]

        resp_data = b""
        while len(resp_data) < resp_len:
            chunk = sock.recv(resp_len - len(resp_data))
            if not chunk:
                raise ConnectionError("Connection closed before full response received")
            resp_data += chunk

    return zlib.decompress(resp_data).decode("utf-8")
xml_request = """<?xml version="1.0"?>
<sirena>
  <query>
    <booking>
      <segment>
        <company>ТФ</company>
        <flight>959</flight>
        <departure>БИШ</departure>
        <arrival>ДМД</arrival>
        <date>30.06.25</date>
        <subclass>О</subclass>
      </segment>
      <passenger>
        <lastname>IVANOV</lastname>
        <firstname>VASILIY PETROVICH</firstname>
        <birthdate>01.06.78</birthdate>
        <sex>male</sex>
        <category>ААА</category>
        <doccode>ПС</doccode>
        <doc>1234561234</doc>
        <doc_country>РФ</doc_country>
      </passenger>
      <customer>
        <phone type="mobile">79101234567</phone>
        <email>webhelp@sirena-travel.ru</email>
      </customer>
    </booking>
  </query>
</sirena>"""


if __name__ == "__main__":
    response = send_tcp_request(xml_request)
    print(response)
