

def __read_gflags_from_env__():
    '\n    Enable reading gflags from environment variables.\n    \n    Returns:\n        None\n    '
    import sys
    import core
    read_env_flags = ['use_pinned_memory']
    if core.is_compile_gpu():
        read_env_flags.append('fraction_of_gpu_memory_to_use')
    core.init_gflags((sys.argv + [('--tryfromenv=' + ','.join(read_env_flags))]))
