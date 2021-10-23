def container_stop(self, container_id):
    if self.parameters.force_kill:
        self.container_kill(container_id)
        return
    self.results['actions'].append(dict(stopped=container_id, timeout=self.parameters.stop_timeout))
    self.results['changed'] = True
    response = None
    if (not self.check_mode):
        count = 0
        while True:
            try:
                if self.parameters.stop_timeout:
                    response = self.client.stop(container_id, timeout=self.parameters.stop_timeout)
                else:
                    response = self.client.stop(container_id)
            except APIError as exc:
                if ('Unpause the container before stopping or killing' in exc.explanation):
                    if (count == 3):
                        self.fail(('Error removing container %s (tried to unpause three times): %s' % (container_id, str(exc))))
                    count += 1
                    try:
                        self.client.unpause(container=container_id)
                    except Exception as exc2:
                        self.fail(('Error unpausing container %s for removal: %s' % (container_id, str(exc2))))
                    continue
                self.fail(('Error stopping container %s: %s' % (container_id, str(exc))))
            except Exception as exc:
                self.fail(('Error stopping container %s: %s' % (container_id, str(exc))))
            break
    return response