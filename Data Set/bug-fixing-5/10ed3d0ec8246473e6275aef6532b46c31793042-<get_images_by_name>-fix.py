def get_images_by_name(module, client, name_pattern):
    images = []
    pattern = None
    pool = get_all_images(client)
    if name_pattern.startswith('~'):
        import re
        if (name_pattern[1] == '*'):
            pattern = re.compile(name_pattern[2:], re.IGNORECASE)
        else:
            pattern = re.compile(name_pattern[1:])
    for image in pool.IMAGE:
        if (pattern is not None):
            if pattern.match(image.NAME):
                images.append(image)
        elif (name_pattern == image.NAME):
            images.append(image)
            break
    if ((pattern is None) and (len(images) == 0)):
        module.fail_json(msg=('There is no IMAGE with name=' + name_pattern))
    return images