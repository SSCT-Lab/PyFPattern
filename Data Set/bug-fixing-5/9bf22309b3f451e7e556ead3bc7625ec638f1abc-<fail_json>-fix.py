def fail_json(self, **kwargs):
    ' return from the module, with an error message '
    if ('msg' not in kwargs):
        raise AssertionError('implementation error -- msg to explain the error is required')
    kwargs['failed'] = True
    if (('exception' not in kwargs) and sys.exc_info()[2] and (self._debug or (self._verbosity >= 3))):
        if PY2:
            kwargs['exception'] = ('WARNING: The below traceback may *not* be related to the actual failure.\n' + ''.join(traceback.format_tb(sys.exc_info()[2])))
        else:
            kwargs['exception'] = ''.join(traceback.format_tb(sys.exc_info()[2]))
    self.do_cleanup_files()
    self._return_formatted(kwargs)
    sys.exit(1)