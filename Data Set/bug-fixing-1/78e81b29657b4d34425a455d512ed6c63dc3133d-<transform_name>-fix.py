

def transform_name(partition='', name='', sub_path=''):
    if (partition != ''):
        if name.startswith((partition + '/')):
            name = name.replace((partition + '/'), '')
        if name.startswith((('/' + partition) + '/')):
            name = name.replace((('/' + partition) + '/'), '')
    if name:
        name = name.replace('/', '~')
    if partition:
        partition = partition.replace('/', '~')
        if (not partition.startswith('~')):
            partition = ('~' + partition)
    elif sub_path:
        raise F5ModuleError('When giving the subPath component include partition as well.')
    if (sub_path and partition):
        sub_path = ('~' + sub_path)
    if (name and partition):
        name = ('~' + name)
    result = ((partition + sub_path) + name)
    return result
