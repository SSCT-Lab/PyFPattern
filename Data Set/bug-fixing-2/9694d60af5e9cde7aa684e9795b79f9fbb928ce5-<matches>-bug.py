

def matches(self, value):
    match = re.search(value, self.value, re.M)
    return (match is not None)
