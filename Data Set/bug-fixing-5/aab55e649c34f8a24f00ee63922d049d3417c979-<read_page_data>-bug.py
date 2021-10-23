def read_page_data(page_data, type):
    assert (type in ['classes', 'functions'])
    data = page_data.get(type, [])
    for module in page_data.get('all_module_{}'.format(type), []):
        module_data = []
        for name in dir(module):
            if ((name[0] == '_') or (name in EXCLUDE)):
                continue
            module_member = getattr(module, name)
            if ((inspect.isclass(module_member) and (type == 'classes')) or (inspect.isfunction(module_member) and (type == 'functions'))):
                instance = module_member
                if (module.__name__ in instance.__module__):
                    if (instance not in module_data):
                        module_data.append(instance)
        module_data.sort(key=(lambda x: id(x)))
        data += module_data
    return data