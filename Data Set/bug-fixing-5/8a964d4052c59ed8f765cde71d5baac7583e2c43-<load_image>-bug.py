def load_image(self):
    '\n        Load an image from a .tar archive\n\n        :return: image dict\n        '
    try:
        self.log(('Opening image %s' % self.load_path))
        image_tar = open(self.load_path, 'r')
    except Exception as exc:
        self.fail(('Error opening image %s - %s' % (self.load_path, str(exc))))
    try:
        self.log(('Loading image from %s' % self.load_path))
        self.client.load_image(image_tar)
    except Exception as exc:
        self.fail(('Error loading image %s - %s' % (self.name, str(exc))))
    try:
        image_tar.close()
    except Exception as exc:
        self.fail(('Error closing image %s - %s' % (self.name, str(exc))))
    return self.client.find_image(self.name, self.tag)