def container_stop(self, container_id):
    if self.parameters.force_kill:
        self.container_kill(container_id)
        return
    self.results['actions'].append(dict(stopped=container_id, timeout=self.parameters.stop_timeout))
    self.results['changed'] = True
    response = None
    if (not self.check_mode):
        try:
            if self.parameters.stop_timeout:
                response = self.client.stop(container_id, timeout=self.parameters.stop_timeout)
            else:
                response = self.client.stop(container_id)
        except Exception as exc:
            self.fail(('Error stopping container %s: %s' % (container_id, str(exc))))
    return response