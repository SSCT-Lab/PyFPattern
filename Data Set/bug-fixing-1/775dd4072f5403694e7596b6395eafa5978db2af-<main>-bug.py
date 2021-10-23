

def main(filename):
    if (not os.path.isfile(filename)):
        return
    tree = et.parse(filename)
    root = tree.getroot()
    current_class = ''
    for el in root.findall('testcase'):
        cn = el.attrib['classname']
        for sk in el.findall('skipped'):
            old_class = current_class
            current_class = cn
            if (old_class != current_class):
                (yield None)
            (yield {
                'class_name': current_class,
                'test_name': el.attrib['name'],
                'message': sk.attrib['message'],
            })
