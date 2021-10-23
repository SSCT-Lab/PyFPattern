def declare_outputs():
    files = ['Declarations.yaml', 'Type.h', 'Type.cpp', 'Tensor.h', 'TensorMethods.h', 'Functions.h', 'Copy.cpp', 'NativeFunctions.h']
    for f in files:
        file_manager.will_write(f)
    for fname in sorted(generators.keys()):
        file_manager.will_write(fname)
    for (backend, density, scalar_types) in iterate_types():
        scalar_name = scalar_types[0]
        full_backend = (('Sparse' + backend) if (density == 'Sparse') else backend)
        for kind in ['Storage', 'Type', 'Tensor']:
            if ((kind == 'Storage') and (density == 'Sparse')):
                continue
            file_manager.will_write('{}{}{}.h'.format(full_backend, scalar_name, kind))
            file_manager.will_write('{}{}{}.cpp'.format(full_backend, scalar_name, kind))