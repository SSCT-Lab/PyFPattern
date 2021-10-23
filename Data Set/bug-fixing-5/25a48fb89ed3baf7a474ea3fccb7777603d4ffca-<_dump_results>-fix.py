def _dump_results(self, result, indent=None, sort_keys=True, keep_invocation=False):
    if result.get('_ansible_no_log', False):
        return json.dumps(dict(censored="the output has been hidden due to the fact that 'no_log: true' was specified for this result"))
    abridged_result = strip_internal_keys(result)
    if ((not keep_invocation) and (self._display.verbosity < 3) and ('invocation' in result)):
        del abridged_result['invocation']
    if ((self._display.verbosity < 3) and ('diff' in result)):
        del abridged_result['diff']
    if ('exception' in abridged_result):
        del abridged_result['exception']
    dumped = ''
    if ('changed' in abridged_result):
        dumped += (('changed=' + str(abridged_result['changed']).lower()) + ' ')
        del abridged_result['changed']
    if ('skipped' in abridged_result):
        dumped += (('skipped=' + str(abridged_result['skipped']).lower()) + ' ')
        del abridged_result['skipped']
    if (('stdout' in abridged_result) and ('stdout_lines' in abridged_result)):
        abridged_result['stdout_lines'] = '<omitted>'
    if abridged_result:
        dumped += '\n'
        dumped += to_text(yaml.dump(abridged_result, allow_unicode=True, width=1000, Dumper=AnsibleDumper, default_flow_style=False))
    dumped = '\n  '.join(dumped.split('\n')).rstrip()
    return dumped