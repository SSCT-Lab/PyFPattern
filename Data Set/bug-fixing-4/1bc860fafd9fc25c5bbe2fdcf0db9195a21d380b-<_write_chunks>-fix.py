def _write_chunks(self, response, filehandle, chunk_size=8192, report_hook=None):
    total_size = response.info().get('Content-Length').strip()
    total_size = int(total_size)
    bytes_so_far = 0
    while True:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)
        if (not chunk):
            break
        filehandle.write(chunk)
        if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)
    return bytes_so_far