

def set_config(**kwargs):
    'Set up the configure of profiler (only accepts keyword arguments).\n\n    Parameters\n    ----------\n    filename : string,\n        output file for profile data\n    profile_all : boolean,\n        all profile types enabled\n    profile_symbolic : boolean,\n        whether to profile symbolic operators\n    profile_imperative : boolean,\n        whether to profile imperative operators\n    profile_memory : boolean,\n        whether to profile memory usage\n    profile_api : boolean,\n        whether to profile the C API\n    continuous_dump : boolean,\n        whether to periodically dump profiling data to file\n    dump_period : float,\n        seconds between profile data dumps\n    aggregate_stats : boolean,\n        whether to maintain aggregate stats in memory for console\n        dump.  Has some negative performance impact.\n    profile_process : string\n        whether to profile kvstore `server` or `worker`.\n        server can only be profiled when kvstore is of type dist.\n        if this is not passed, defaults to `worker`\n    '
    kk = kwargs.keys()
    vv = kwargs.values()
    check_call(_LIB.MXSetProcessProfilerConfig(len(kwargs), c_str_array([key for key in kk]), c_str_array([str(val) for val in vv]), profiler_kvstore_handle))
