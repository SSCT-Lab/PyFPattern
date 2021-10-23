def present(self, state):
    container = self._get_container(self.parameters.name)
    image = self._get_image()
    self.log(image, pretty_print=True)
    if (not container.exists):
        self.log('No container found')
        if (not self.parameters.image):
            self.fail('Cannot create container when image is not specified!')
        new_container = self.container_create(self.parameters.image, self.parameters.create_parameters)
        if new_container:
            container = new_container
    else:
        (different, differences) = container.has_different_configuration(image)
        image_different = False
        if (self.parameters.comparisons['image']['comparison'] == 'strict'):
            image_different = self._image_is_different(image, container)
        if (image_different or different or self.parameters.recreate):
            self.diff['differences'] = differences
            if image_different:
                self.diff['image_different'] = True
            self.log('differences')
            self.log(differences, pretty_print=True)
            image_to_use = self.parameters.image
            if ((not image_to_use) and container and container.Image):
                image_to_use = container.Image
            if (not image_to_use):
                self.fail('Cannot recreate container when image is not specified or cannot be extracted from current container!')
            if container.running:
                self.container_stop(container.Id)
            self.container_remove(container.Id)
            new_container = self.container_create(image_to_use, self.parameters.create_parameters)
            if new_container:
                container = new_container
    if (container and container.exists):
        container = self.update_limits(container)
        container = self.update_networks(container)
        if ((state == 'started') and (not container.running)):
            container = self.container_start(container.Id)
        elif ((state == 'started') and self.parameters.restart):
            self.container_stop(container.Id)
            container = self.container_start(container.Id)
        elif ((state == 'stopped') and container.running):
            self.container_stop(container.Id)
            container = self._get_container(container.Id)
        if ((state == 'started') and (container.paused != self.parameters.paused)):
            if (not self.check_mode):
                try:
                    if self.parameters.paused:
                        self.client.pause(container=container.Id)
                    else:
                        self.client.unpause(container=container.Id)
                except Exception as exc:
                    self.fail(('Error %s container %s: %s' % (('pausing' if self.parameters.paused else 'unpausing'), container.Id, str(exc))))
                container = self._get_container(container.Id)
            self.results['changed'] = True
            self.results['actions'].append(dict(set_paused=self.parameters.paused))
    self.facts = container.raw