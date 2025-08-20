import csv
from typing import Iterable, Iterator, List

def rows_to_csv_bytes(rows: Iterable[List[str]]) -> Iterator[bytes]:
    import io
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, delimiter=",")
    for row in rows:
        writer.writerow(row)
        data = buf.getvalue()
        if data:
            yield data.encode("cp1252", errors="replace")
            buf.seek(0); buf.truncate(0)
