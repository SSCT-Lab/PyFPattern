

def transform_name(partition='', name='', sub_path=''):
    if name:
        name = name.replace('/', '~')
    if partition:
        partition = ('~' + partition)
    elif sub_path:
        raise F5ModuleError('When giving the subPath component include partition as well.')
    if (sub_path and partition):
        sub_path = ('~' + sub_path)
    if (name and partition):
        name = ('~' + name)
    result = ((partition + sub_path) + name)
    return result
