#!/usr/bin/env python3
from pathlib import Path
import csv
from parser import parse_xml
import sys

def process(input:Path, output:Path) -> None:
    invoices = parse_xml(input)

    with output.open('w') as csv_file:
        fieldnames = invoices[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for invoice in invoices:
            writer.writerow(invoice)

if __name__ == "__main__":
    input = Path(sys.argv[1])
    output = Path(sys.argv[2])

    process(input, output)
