import socket 


def send_xml_to_sirena(xml: str, host: str, port: str, timeout=10) -> str:
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.sendall(xml.encode('utf-8'))

        response = b""
        while True:
            part = sock.recv(4096)
            if not part:
                break
            response += part

        return response.decode('utf-8')
