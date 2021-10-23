def _wait_for_creation(self, resource, result):
    return_obj = None
    desired_cdi_status = 'Succeeded'
    uid = result['metadata']['uid']
    use_cdi = (True if self.params.get('cdi_source') else False)
    if (use_cdi and ('upload' in self.params['cdi_source'])):
        desired_cdi_status = 'Running'
    if (not use_cdi):
        v1_events = self.client.resources.get(api_version='v1', kind='Event')
        pvc_events = v1_events.get(namespace=self.namespace, field_selector='involvedObject.uid={0}'.format(uid))
        reasons = [item.reason for item in pvc_events.items if hasattr(item, 'reason')]
        if ('WaitForFirstConsumer' in reasons):
            return result
    for event in resource.watch(namespace=self.namespace, field_selector='involvedObject.uid={0}'.format(uid), timeout=self.params.get('wait_timeout')):
        entity = event['object']
        metadata = entity.metadata
        if (entity.status.phase == 'Bound'):
            if (use_cdi and hasattr(metadata, 'annotations')):
                import_status = metadata.annotations.get('cdi.kubevirt.io/storage.pod.phase')
                if (import_status == desired_cdi_status):
                    return_obj = entity
                    break
            else:
                return_obj = entity
                break
        elif (entity.status.phase == 'Failed'):
            raise CreatePVCFailed('PVC creation failed')
    if (not return_obj):
        raise CreatePVCFailed('PVC creation timed out')
    return self.fix_serialization(return_obj)