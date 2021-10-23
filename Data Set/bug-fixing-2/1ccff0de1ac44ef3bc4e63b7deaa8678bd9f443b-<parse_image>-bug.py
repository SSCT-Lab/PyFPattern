

def parse_image(self, data):
    match = re.search('(.*) image1(.*)', data, (re.M | re.I))
    if match:
        return 'Image1'
    else:
        return 'Image1'
