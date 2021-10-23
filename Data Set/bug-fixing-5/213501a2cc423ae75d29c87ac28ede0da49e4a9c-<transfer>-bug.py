def transfer(connection, module, direction, transfer_func):
    transfers_service = connection.system_service().image_transfers_service()
    transfer = transfers_service.add(otypes.ImageTransfer(image=otypes.Image(id=module.params['id']), direction=direction))
    transfer_service = transfers_service.image_transfer_service(transfer.id)
    try:
        while (transfer.phase == otypes.ImageTransferPhase.INITIALIZING):
            time.sleep(module.params['poll_interval'])
            transfer = transfer_service.get()
        proxy_url = urlparse(transfer.proxy_url)
        context = ssl.create_default_context()
        auth = module.params['auth']
        if auth.get('insecure'):
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        elif auth.get('ca_file'):
            context.load_verify_locations(cafile=auth.get('ca_file'))
        proxy_connection = HTTPSConnection(proxy_url.hostname, proxy_url.port, context=context)
        transfer_func(transfer_service, proxy_connection, proxy_url, transfer.signed_ticket)
        return True
    finally:
        transfer_service.finalize()
        while (transfer.phase in [otypes.ImageTransferPhase.TRANSFERRING, otypes.ImageTransferPhase.FINALIZING_SUCCESS]):
            time.sleep(module.params['poll_interval'])
            transfer = transfer_service.get()
        if (transfer.phase in [otypes.ImageTransferPhase.UNKNOWN, otypes.ImageTransferPhase.FINISHED_FAILURE, otypes.ImageTransferPhase.FINALIZING_FAILURE, otypes.ImageTransferPhase.CANCELLED]):
            raise Exception(('Error occurred while uploading image. The transfer is in %s' % transfer.phase))
        if module.params.get('logical_unit'):
            disks_service = connection.system_service().disks_service()
            wait(service=disks_service.service(module.params['id']), condition=(lambda d: (d.status == otypes.DiskStatus.OK)), wait=module.params['wait'], timeout=module.params['timeout'])