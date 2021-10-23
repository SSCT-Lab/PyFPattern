

def archive_image(self, name, tag):
    '\n        Archive an image to a .tar file. Called when archive_path is passed.\n\n        :param name - name of the image. Type: str\n        :return None\n        '
    if (not tag):
        tag = 'latest'
    image = self.client.find_image(name=name, tag=tag)
    if (not image):
        self.log(('archive image: image %s:%s not found' % (name, tag)))
        return
    image_name = ('%s:%s' % (name, tag))
    self.results['actions'].append(('Archived image %s to %s' % (image_name, self.archive_path)))
    self.results['changed'] = True
    if (not self.check_mode):
        self.log(('Getting archive of image %s' % image_name))
        try:
            image = self.client.get_image(image_name)
        except Exception as exc:
            self.fail(('Error getting image %s - %s' % (image_name, str(exc))))
        try:
            with open(self.archive_path, 'w') as fd:
                for chunk in image.stream(2048, decode_content=False):
                    fd.write(chunk)
        except Exception as exc:
            self.fail(('Error writing image archive %s - %s' % (self.archive_path, str(exc))))
    image = self.client.find_image(name=name, tag=tag)
    if image:
        self.results['image'] = image
