def upload_disk_image(connection, module):

    def _transfer(transfer_service, proxy_connection, proxy_url, transfer_ticket):
        BUF_SIZE = (128 * 1024)
        path = module.params['upload_image_path']
        image_size = os.path.getsize(path)
        proxy_connection.putrequest('PUT', proxy_url.path)
        proxy_connection.putheader('Content-Length', ('%d' % (image_size,)))
        proxy_connection.endheaders()
        with open(path, 'rb') as disk:
            pos = 0
            while (pos < image_size):
                to_read = min((image_size - pos), BUF_SIZE)
                chunk = disk.read(to_read)
                if (not chunk):
                    transfer_service.pause()
                    raise RuntimeError(('Unexpected end of file at pos=%d' % pos))
                proxy_connection.send(chunk)
                pos += len(chunk)
    return transfer(connection, module, otypes.ImageTransferDirection.UPLOAD, transfer_func=_transfer)