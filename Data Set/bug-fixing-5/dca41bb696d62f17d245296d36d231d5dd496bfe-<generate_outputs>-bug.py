def generate_outputs():
    cwrap_files = filter_by_extension(options.files, '.cwrap')
    nn_files = filter_by_extension(options.files, 'nn.yaml', '.h')
    native_files = filter_by_extension(options.files, 'native_functions.yaml')
    declarations = [d for file in cwrap_files for d in cwrap_parser.parse(file)]
    declarations += nn_parse.run(nn_files)
    declarations += native_parse.run(native_files)
    declarations = preprocess_declarations.run(declarations)
    for (fname, env) in generators.items():
        file_manager.write(fname, GENERATOR_DERIVED.substitute(env))
    output_declarations = function_wrapper.create_generic(top_env, declarations)
    output_declarations = postprocess_output_declarations(output_declarations)
    file_manager.write('Declarations.yaml', format_yaml(output_declarations))
    all_types = []
    for (backend, density, scalar_type) in iterate_types():
        all_types.append(generate_storage_type_and_tensor(backend, density, scalar_type, declarations))
    file_manager.write('Type.h', TYPE_H.substitute(top_env))
    file_manager.write('Type.cpp', TYPE_CPP.substitute(top_env))
    file_manager.write('Tensor.h', TENSOR_H.substitute(top_env))
    file_manager.write('TensorMethods.h', TENSOR_METHODS_H.substitute(top_env))
    file_manager.write('Functions.h', FUNCTIONS_H.substitute(top_env))
    file_manager.write('Copy.cpp', copy_wrapper.create(all_types))
    file_manager.write('NativeFunctions.h', NATIVE_FUNCTIONS_H.substitute(top_env))
    file_manager.check_all_files_written()