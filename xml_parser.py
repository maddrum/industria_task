from urllib import request
import xml.etree.ElementTree as ET


def get_currency_values():
    """Returns current values of currencies from BNB site"""
    url_str = 'http://bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm?download=xml&search=&lang=BG'
    xml_str = request.urlopen(url_str).read()
    root = ET.fromstring(xml_str)
    result = {}
    for item in root:
        temp_dict = {}
        temp_dict['units'] = item[3].text
        try:
            temp_dict['rate'] = float(item[5].text)
        except ValueError:
            continue
        code = item[2].text
        result[code] = temp_dict
    return result
