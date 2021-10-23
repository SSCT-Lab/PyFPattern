

def visit_member(parent_name, member):
    cur_name = '.'.join([parent_name, member.__name__])
    if inspect.isclass(member):
        for (name, value) in inspect.getmembers(member):
            if (hasattr(value, '__name__') and ((not name.startswith('_')) or (name == '__init__'))):
                visit_member(cur_name, value)
    elif callable(member):
        try:
            doc = ('document', md5(member.__doc__))
            args = inspect.getargspec(member)
            all = (args, doc)
            member_dict[cur_name] = all
        except TypeError:
            member_dict[cur_name] = '  '.join([line.strip() for line in pydoc.render_doc(member).split('\n') if ('->' in line)])
    elif inspect.isgetsetdescriptor(member):
        return
    else:
        raise RuntimeError('Unsupported generate signature of member, type {0}'.format(str(type(member))))
