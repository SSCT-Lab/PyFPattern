def _determine_error_states():
    global _linalg_error_extobj
    errobj = geterrobj()
    bufsize = errobj[0]
    with errstate(invalid='call', over='ignore', divide='ignore', under='ignore'):
        invalid_call_errmask = geterrobj()[1]
    _linalg_error_extobj = [bufsize, invalid_call_errmask, None]