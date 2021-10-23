def build_image(self):
    '\n        Build an image\n\n        :return: image dict\n        '
    params = dict(path=self.path, tag=self.name, rm=self.rm, nocache=self.nocache, stream=True, timeout=self.http_timeout, pull=self.pull, forcerm=self.rm, dockerfile=self.dockerfile, decode=True)
    if self.tag:
        params['tag'] = ('%s:%s' % (self.name, self.tag))
    if self.container_limits:
        params['container_limits'] = self.container_limits
    if self.buildargs:
        for (key, value) in self.buildargs.items():
            if (not isinstance(value, basestring)):
                self.buildargs[key] = str(value)
        params['buildargs'] = self.buildargs
    for line in self.client.build(**params):
        self.log(line, pretty_print=True)
        if line.get('error'):
            if line.get('errorDetail'):
                errorDetail = line.get('errorDetail')
                self.fail(('Error building %s - code: %s message: %s' % (self.name, errorDetail.get('code'), errorDetail.get('message'))))
            else:
                self.fail(('Error building %s - %s' % (self.name, line.get('error'))))
    return self.client.find_image(name=self.name, tag=self.tag)