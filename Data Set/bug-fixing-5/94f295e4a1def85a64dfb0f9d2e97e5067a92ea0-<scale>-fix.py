def scale(self, resource, existing_object, replicas, wait, wait_time):
    name = existing_object.metadata.name
    namespace = existing_object.metadata.namespace
    if (not hasattr(resource, 'scale')):
        self.fail_json(msg='Cannot perform scale on resource of kind {0}'.format(resource.kind))
    scale_obj = {
        'metadata': {
            'name': name,
            'namespace': namespace,
        },
        'spec': {
            'replicas': replicas,
        },
    }
    return_obj = None
    stream = None
    if wait:
        (w, stream) = self._create_stream(resource, namespace, wait_time)
    try:
        resource.scale.patch(body=scale_obj)
    except Exception as exc:
        self.fail_json(msg='Scale request failed: {0}'.format(exc))
    if (wait and (stream is not None)):
        return_obj = self._read_stream(resource, w, stream, name, replicas)
    if (not return_obj):
        return_obj = self._wait_for_response(resource, name, namespace)
    return return_obj