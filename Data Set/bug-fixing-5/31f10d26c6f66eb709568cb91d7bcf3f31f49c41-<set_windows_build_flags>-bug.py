def set_windows_build_flags(environ_cp):
    'Set Windows specific build options.'
    write_to_bazelrc('build --config monolithic')
    write_to_bazelrc('build --copt=-w --host_copt=-w')
    write_to_bazelrc('build --verbose_failures')
    write_to_bazelrc('build --distinct_host_configuration=false')
    write_to_bazelrc('build --experimental_shortened_obj_file_path=true')
    if get_var(environ_cp, 'TF_OVERRIDE_EIGEN_STRONG_INLINE', 'Eigen strong inline', True, 'Would you like to override eigen strong inline for some C++ compilation to reduce the compilation time?', 'Eigen strong inline overridden.', 'Not overriding eigen strong inline, some compilations could take more than 20 mins.'):
        write_to_bazelrc('build --define=override_eigen_strong_inline=true')