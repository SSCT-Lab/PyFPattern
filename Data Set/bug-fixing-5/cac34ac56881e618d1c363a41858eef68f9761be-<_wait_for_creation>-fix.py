def _wait_for_creation(self, resource, uid):
    return_obj = None
    desired_cdi_status = 'Succeeded'
    use_cdi = (True if self.params.get('cdi_source') else False)
    if (use_cdi and ('upload' in self.params['cdi_source'])):
        desired_cdi_status = 'Running'
    for event in resource.watch(namespace=self.namespace, timeout=self.params.get('wait_timeout')):
        entity = event['object']
        metadata = entity.metadata
        if ((not hasattr(metadata, 'uid')) or (metadata.uid != uid)):
            continue
        if (entity.status.phase == 'Bound'):
            if (use_cdi and hasattr(metadata, 'annotations')):
                import_status = metadata.annotations.get('cdi.kubevirt.io/storage.pod.phase')
                if (import_status == desired_cdi_status):
                    return_obj = entity
                    break
                elif (import_status == 'Failed'):
                    raise CreatePVCFailed('PVC creation incomplete; importing data failed')
            else:
                return_obj = entity
                break
        elif (entity.status.phase == 'Failed'):
            raise CreatePVCFailed('PVC creation failed')
    if (not return_obj):
        raise CreatePVCFailed('PVC creation timed out')
    return self.fix_serialization(return_obj)