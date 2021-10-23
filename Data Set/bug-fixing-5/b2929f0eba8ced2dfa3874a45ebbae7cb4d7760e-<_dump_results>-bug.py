def _dump_results(self, result, indent=None, sort_keys=True, keep_invocation=False):
    if ((not indent) and (result.get('_ansible_verbose_always') or (self._display.verbosity > 2))):
        indent = 4
    abridged_result = strip_internal_keys(result)
    if ((not keep_invocation) and (self._display.verbosity < 3) and ('invocation' in result)):
        del abridged_result['invocation']
    if ((self._display.verbosity < 3) and ('diff' in result)):
        del abridged_result['diff']
    if ('exception' in abridged_result):
        del abridged_result['exception']
    return json.dumps(abridged_result, indent=indent, ensure_ascii=False, sort_keys=sort_keys)