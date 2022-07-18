from xml.dom.minidom import parse, Element
import re
from pathlib import Path
from typing import Dict, List


def parse_xml(input: Path) -> List[Dict[str, str]]:
    with input.open() as f:
        document = parse(f)

    records = []
    for invoice in document.getElementsByTagName('Invoice'):
        records.append(parse_invoice(invoice))

    return records


def parse_invoice(invoice: Element) -> Dict[str, str]:
    record = {}

    record['invoiceId'] = re.findall('P(\d+)', invoice.getAttribute('invoiceId'))[0]
    record['serviceId'] = invoice.getAttribute('serviceId')
    record['channelAddress'] = invoice.getAttribute('channelAddress')
    record['globalSellerContractId'] = invoice.getAttribute('globalSellerContractId')
    record['BuyerParty_name'] = invoice \
        .getElementsByTagName('BuyerParty')[0] \
        .getElementsByTagName('Name')[0] \
        .firstChild.data
    invoice_nr = invoice \
        .getElementsByTagName('InvoiceInformation')[0] \
        .getElementsByTagName('InvoiceNumber')[0] \
        .firstChild.data
    record['InvoiceNumber'] = re.findall('P Nr. (\d+)', invoice_nr)[0]
    record['InvoiceDate'] = invoice \
        .getElementsByTagName('InvoiceInformation')[0] \
        .getElementsByTagName('InvoiceDate')[0] \
        .firstChild.data
    record['TotalSum'] = invoice \
        .getElementsByTagName('InvoiceSumGroup')[0] \
        .getElementsByTagName('TotalSum')[0] \
        .firstChild.data

    description = invoice \
        .getElementsByTagName('PaymentInfo')[0] \
        .getElementsByTagName('PaymentDescription')[0] \
        .firstChild.data

    striped_d = re.findall(r'(.+bt\. )', description)
    record['Description'] = striped_d[0] if striped_d else description

    record['PayDueDate'] = invoice \
        .getElementsByTagName('PaymentInfo')[0] \
        .getElementsByTagName('PayDueDate')[0] \
        .firstChild.data
    record['PaymentTotalSum'] = invoice \
        .getElementsByTagName('PaymentInfo')[0] \
        .getElementsByTagName('PaymentTotalSum')[0] \
        .firstChild.data
    record['PaymentId'] = invoice \
        .getElementsByTagName('PaymentInfo')[0] \
        .getElementsByTagName('PaymentId')[0] \
        .firstChild.data

    return record
