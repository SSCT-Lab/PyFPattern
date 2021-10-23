def present(self):
    "\n        Handles state = 'present', which includes building, loading or pulling an image,\n        depending on user provided parameters.\n\n        :returns None\n        "
    image = self.client.find_image(name=self.name, tag=self.tag)
    if ((not image) or self.force):
        if self.path:
            if (not os.path.isdir(self.path)):
                self.fail(('Requested build path %s could not be found or you do not have access.' % self.path))
            image_name = self.name
            if self.tag:
                image_name = ('%s:%s' % (self.name, self.tag))
            self.log(('Building image %s' % image_name))
            self.results['actions'].append(('Built image %s from %s' % (image_name, self.path)))
            self.results['changed'] = True
            if (not self.check_mode):
                self.results['image'] = self.build_image()
        elif self.load_path:
            if (not os.path.isfile(self.load_path)):
                self.fail(('Error loading image %s. Specified path %s does not exist.' % (self.name, self.load_path)))
            image_name = self.name
            if self.tag:
                image_name = ('%s:%s' % (self.name, self.tag))
            self.results['actions'].append(('Loaded image %s from %s' % (image_name, self.load_path)))
            self.results['changed'] = True
            if (not self.check_mode):
                self.results['image'] = self.load_image()
        else:
            self.results['actions'].append(('Pulled image %s:%s' % (self.name, self.tag)))
            self.results['changed'] = True
            if (not self.check_mode):
                self.results['image'] = self.client.pull_image(self.name, tag=self.tag)
                if (image and (image == self.results['image'])):
                    self.results['changed'] = False
    if self.archive_path:
        self.archive_image(self.name, self.tag)
    if (self.push and (not self.repository)):
        self.push_image(self.name, self.tag)
    elif self.repository:
        self.tag_image(self.name, self.tag, self.repository, force=self.force, push=self.push)