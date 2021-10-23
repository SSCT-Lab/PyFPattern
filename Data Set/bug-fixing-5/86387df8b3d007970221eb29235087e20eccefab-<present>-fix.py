def present(self, state):
    container = self._get_container(self.parameters.name)
    if self.parameters.image:
        image = self._get_image()
        self.log(image, pretty_print=True)
        if (not container.exists):
            self.log('No container found')
            new_container = self.container_create(self.parameters.image, self.parameters.create_parameters)
            if new_container:
                container = new_container
        else:
            (different, differences) = container.has_different_configuration(image)
            image_different = False
            if (not self.parameters.ignore_image):
                image_different = self._image_is_different(image, container)
            if (image_different or different or self.parameters.recreate):
                self.diff['differences'] = differences
                if image_different:
                    self.diff['image_different'] = True
                self.log('differences')
                self.log(differences, pretty_print=True)
                if container.running:
                    self.container_stop(container.Id)
                self.container_remove(container.Id)
                new_container = self.container_create(self.parameters.image, self.parameters.create_parameters)
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
    self.facts = container.raw