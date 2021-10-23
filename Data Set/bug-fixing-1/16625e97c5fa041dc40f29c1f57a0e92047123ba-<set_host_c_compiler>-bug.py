

def set_host_c_compiler(environ_cp):
    'Set HOST_C_COMPILER.'
    default_c_host_compiler = (which('gcc') or '')
    host_c_compiler = prompt_loop_or_load_from_env(environ_cp, var_name='HOST_C_COMPILER', var_default=default_c_host_compiler, ask_for_var='Please specify which C compiler should be used as the hostC compiler.', check_success=os.path.exists, error_msg='Invalid C compiler path. %s cannot be found.')
    write_action_env_to_bazelrc('HOST_C_COMPILER', host_c_compiler)
