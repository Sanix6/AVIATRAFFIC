from lxml import etree

def get_connected_cities(instance_name, q):
    root = etree.Element('sirena')
    query = etree.SubElement(root, 'query')
    connected = etree.SubElement(query, 'connected_cities')
    etree.SubElement(connected, 'point').text = q.get('point')
    etree.SubElement(connected, 'from').text = q.get('from')
    etree.SubElement(connected, 'to').text = q.get('to')

    return etree.tostring(root, pretty_print=True, encoding='UTF-8', xml_declaration=True)


def pars_connected_cities(xml_bytes):
    root = etree.fromstring(xml_bytes)
    connected = root.find('.//connected_cities')

    result = {}

    cities_to = connected.find('cities_to')
    if cities_to is not None:
        result['cities_to'] = [city.text for city in cities_to.findall('city')]

    cities_from = connected.find('cities_from')
    if cities_from is not None:
        result['cities_from'] = [city.text for city in cities_from.findall('city')]

    return result

