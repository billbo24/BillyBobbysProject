import csv
from typing import Iterable

def read_csv(filePath: str, skip_headers: bool = True, encoding: str = None) -> Iterable[str]:
    with open(filePath, 'r', encoding=encoding) as file:
        csv_reader = csv.reader(file)

        if skip_headers:
            next(csv_reader)

        yield from csv_reader

def read_csv_dict(filePath: str, header_conversions: dict[str, str] = None, encoding: str = None) -> Iterable[str]:
    data = read_csv(filePath, skip_headers=False, encoding=encoding)
    headers: dict[str, int] = {header: index for index, header in enumerate(next(data))}

    if header_conversions is not None:
        for original, replacement in header_conversions.items():
            index = headers[original]
            headers.pop(original)
            headers[replacement] = index

    finalHeaders = sorted(headers, key=lambda header: headers[header])

    for row in data:
        yield {header: val for header, val in zip(finalHeaders, row)}