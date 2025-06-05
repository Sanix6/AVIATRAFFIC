import zlib
import socket
import struct
import time

def send_tcp_request(xml_data):
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