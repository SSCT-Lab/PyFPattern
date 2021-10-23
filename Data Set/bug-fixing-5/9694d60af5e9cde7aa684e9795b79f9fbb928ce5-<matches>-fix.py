def matches(self, value):
    match = re.search(self.value, value, re.M)
    return (match is not None)