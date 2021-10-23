def wait_for_replicas(self):
    namespace = self.params.get('namespace')
    wait_timeout = self.params.get('wait_timeout')
    replicas = self.params.get('replicas')
    name = self.name
    resource = self.find_supported_resource(KIND)
    (w, stream) = self._create_stream(resource, namespace, wait_timeout)
    return self._read_stream(resource, w, stream, name, replicas)