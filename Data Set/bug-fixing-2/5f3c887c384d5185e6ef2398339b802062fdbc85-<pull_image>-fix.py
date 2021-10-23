

def pull_image(self, name, tag='latest'):
    '\n        Pull an image\n        '
    self.log(('Pulling image %s:%s' % (name, tag)))
    old_tag = self.find_image(name, tag)
    try:
        for line in self.pull(name, tag=tag, stream=True, decode=True):
            self.log(line, pretty_print=True)
            if line.get('error'):
                if line.get('errorDetail'):
                    error_detail = line.get('errorDetail')
                    self.fail(('Error pulling %s - code: %s message: %s' % (name, error_detail.get('code'), error_detail.get('message'))))
                else:
                    self.fail(('Error pulling %s - %s' % (name, line.get('error'))))
    except Exception as exc:
        self.fail(('Error pulling image %s:%s - %s' % (name, tag, str(exc))))
    new_tag = self.find_image(name, tag)
    return (new_tag, (old_tag == new_tag))
