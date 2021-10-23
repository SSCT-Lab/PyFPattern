def download_disk_image(connection, module):

    def _transfer(transfer_service, proxy_connection, proxy_url, transfer_ticket):
        disks_service = connection.system_service().disks_service()
        disk = disks_service.disk_service(module.params['id']).get()
        size = disk.actual_size
        transfer_headers = {
            'Authorization': transfer_ticket,
        }
        with open(module.params['download_image_path'], 'wb') as mydisk:
            pos = 0
            MiB_per_request = 8
            chunk_size = ((1024 * 1024) * MiB_per_request)
            while (pos < size):
                transfer_service.extend()
                transfer_headers['Range'] = ('bytes=%d-%d' % (pos, (min(size, (pos + chunk_size)) - 1)))
                proxy_connection.request('GET', proxy_url.path, headers=transfer_headers)
                r = proxy_connection.getresponse()
                if (r.status >= 300):
                    raise Exception(('Error: %s' % r.read()))
                try:
                    mydisk.write(r.read())
                except IncompleteRead as e:
                    mydisk.write(e.partial)
                    break
                pos += chunk_size
    return transfer(connection, module, otypes.ImageTransferDirection.DOWNLOAD, transfer_func=_transfer)