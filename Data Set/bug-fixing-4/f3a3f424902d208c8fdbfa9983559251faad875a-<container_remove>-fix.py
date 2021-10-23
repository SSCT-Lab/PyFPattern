def container_remove(self, container_id, link=False, force=False):
    volume_state = (not self.parameters.keep_volumes)
    self.log(('remove container container:%s v:%s link:%s force%s' % (container_id, volume_state, link, force)))
    self.results['actions'].append(dict(removed=container_id, volume_state=volume_state, link=link, force=force))
    self.results['changed'] = True
    response = None
    if (not self.check_mode):
        count = 0
        while True:
            try:
                response = self.client.remove_container(container_id, v=volume_state, link=link, force=force)
            except NotFound as exc:
                pass
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
                if (('removal of container ' in exc.explanation) and (' is already in progress' in exc.explanation)):
                    pass
                else:
                    self.fail(('Error removing container %s: %s' % (container_id, str(exc))))
            except Exception as exc:
                self.fail(('Error removing container %s: %s' % (container_id, str(exc))))
            break
    return response