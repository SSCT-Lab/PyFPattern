

def pull_image(self, name, tag='latest'):
    '\n        Pull an image\n        '
    self.log(('Pulling image %s:%s' % (name, tag)))
    alreadyToLatest = False
    try:
        for line in self.pull(name, tag=tag, stream=True, decode=True):
            self.log(line, pretty_print=True)
            if line.get('status'):
                if line.get('status').startswith('Status: Image is up to date for'):
                    alreadyToLatest = True
            if line.get('error'):
                if line.get('errorDetail'):
                    error_detail = line.get('errorDetail')
                    self.fail(('Error pulling %s - code: %s message: %s' % (name, error_detail.get('code'), error_detail.get('message'))))
                else:
                    self.fail(('Error pulling %s - %s' % (name, line.get('error'))))
    except Exception as exc:
        self.fail(('Error pulling image %s:%s - %s' % (name, tag, str(exc))))
    return (self.find_image(name, tag), alreadyToLatest)
