

def _image_lookup(self, name, tag):
    '\n        Including a tag in the name parameter sent to the docker-py images method does not \n        work consistently. Instead, get the result set for name and manually check if the tag\n        exists.\n        '
    try:
        response = self.images(name=name)
    except Exception as exc:
        self.fail(('Error searching for image %s - %s' % (name, str(exc))))
    images = response
    if tag:
        lookup = ('%s:%s' % (name, tag))
        images = []
        for image in response:
            tags = image.get('RepoTags')
            if (tags and (lookup in tags)):
                images = [image]
                break
    return images
