

@staticmethod
def _generate_resource_prefix():
    '\n        :rtype: str\n        '
    if is_shippable():
        return ('shippable-%s-%s' % (os.environ['SHIPPABLE_BUILD_NUMBER'], os.environ['SHIPPABLE_JOB_NUMBER']))
    node = re.sub('[^a-zA-Z0-9]+', '-', platform.node().split('.')[0]).lower()
    return ('ansible-test-%s-%d' % (node, random.randint(10000000, 99999999)))
