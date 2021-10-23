def parse_image(self, data):
    match = re.search('(.*) image(.*)', data, (re.M | re.I))
    if match:
        return 'Image1'
    else:
        return 'Image2'