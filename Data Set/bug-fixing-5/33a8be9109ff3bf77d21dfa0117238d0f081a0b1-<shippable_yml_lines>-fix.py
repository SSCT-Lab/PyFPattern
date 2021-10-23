@property
def shippable_yml_lines(self):
    '\n        :rtype: list[str]\n        '
    if (not self._shippable_yml_lines):
        with open(self.SHIPPABLE_YML, 'r') as shippable_yml_fd:
            self._shippable_yml_lines = shippable_yml_fd.read().splitlines()
    return self._shippable_yml_lines