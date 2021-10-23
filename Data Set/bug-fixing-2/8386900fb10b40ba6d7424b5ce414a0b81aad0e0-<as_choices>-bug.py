

@classmethod
def as_choices(cls):
    result = []
    for (name, member) in six.iteritems(cls.__members__):
        if (name != member.name):
            continue
        if name.startswith('_'):
            continue
        result.append((member, member.label))
    return tuple(result)
