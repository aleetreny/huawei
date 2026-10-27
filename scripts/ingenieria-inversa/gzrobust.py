"""Read every complete line from gzip files that may hold truncated members (batches stopped mid-write)."""
import zlib


def read_lines(path: str):
    data = open(path, "rb").read()
    i = 0
    while i < len(data):
        d = zlib.decompressobj(31)
        out = []
        j = i
        ok = True
        while j < len(data):
            try:
                out.append(d.decompress(data[j:j + 65536]))
            except zlib.error:
                ok = False
                break
            j += 65536
            if d.eof:
                break
        txt = b"".join(out)
        lines = txt.split(b"\n")
        for ln in lines[:-1] if not txt.endswith(b"\n") else lines:
            if ln:
                yield ln.decode("utf-8", "replace")
        if d.eof and d.unused_data is not None:
            i = len(data) - len(d.unused_data) if j >= len(data) or d.unused_data else j
            # recompute: position just after this member
            consumed = (j - i) if False else None
        nxt = data.find(b"\x1f\x8b\x08", i + 1)
        if d.eof:
            # start of the next member = total input consumed by this member
            used = len(data[i:]) - len(d.unused_data) if d.unused_data else None
            if used is not None:
                i = i + used
                continue
        if nxt < 0:
            break
        i = nxt
