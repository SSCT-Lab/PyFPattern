

def container_start(self, container_id):
    self.log(('start container %s' % container_id))
    self.results['actions'].append(dict(started=container_id))
    self.results['changed'] = True
    if (not self.check_mode):
        try:
            self.client.start(container=container_id)
        except Exception as exc:
            self.fail(('Error starting container %s: %s' % (container_id, str(exc))))
        if (not self.parameters.detach):
            status = self.client.wait(container_id)
            output = self.client.logs(container_id, stdout=True, stderr=True, stream=False, timestamps=False)
            if (status != 0):
                self.fail(output, status=status)
            if self.parameters.cleanup:
                self.container_remove(container_id, force=True)
            insp = self._get_container(container_id)
            if insp.raw:
                insp.raw['Output'] = output
            else:
                insp.raw = dict(Output=output)
            return insp
    return self._get_container(container_id)
