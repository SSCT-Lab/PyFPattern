def upload_disk_image(connection, module):

    def _transfer(transfer_service, proxy_connection, proxy_url, transfer_ticket):
        path = module.params['upload_image_path']
        transfer_headers = {
            'Authorization': transfer_ticket,
        }
        with open(path, 'rb') as disk:
            pos = 0
            MiB_per_request = 8
            size = os.path.getsize(path)
            chunk_size = ((1024 * 1024) * MiB_per_request)
            while (pos < size):
                transfer_service.extend()
                transfer_headers['Content-Range'] = ('bytes %d-%d/%d' % (pos, (min((pos + chunk_size), size) - 1), size))
                proxy_connection.request('PUT', proxy_url.path, disk.read(chunk_size), headers=transfer_headers)
                r = proxy_connection.getresponse()
                if (r.status >= 400):
                    raise Exception('Failed to upload disk image.')
                pos += chunk_size
    return transfer(connection, module, otypes.ImageTransferDirection.UPLOAD, transfer_func=_transfer)