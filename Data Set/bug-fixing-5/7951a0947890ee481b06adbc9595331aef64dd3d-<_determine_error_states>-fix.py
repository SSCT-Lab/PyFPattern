def _determine_error_states():
    errobj = geterrobj()
    bufsize = errobj[0]
    with errstate(invalid='call', over='ignore', divide='ignore', under='ignore'):
        invalid_call_errmask = geterrobj()[1]
    return [bufsize, invalid_call_errmask, None]