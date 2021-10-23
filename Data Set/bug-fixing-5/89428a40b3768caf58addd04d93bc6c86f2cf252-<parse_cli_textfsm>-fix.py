def parse_cli_textfsm(value, template):
    if (not HAS_TEXTFSM):
        raise AnsibleError('parse_cli_textfsm filter requires TextFSM library to be installed')
    if (not isinstance(value, string_types)):
        raise AnsibleError(('parse_cli_textfsm input should be a string, but was given a input of %s' % type(value)))
    if (not os.path.exists(template)):
        raise AnsibleError(('unable to locate parse_cli_textfsm template: %s' % template))
    try:
        template = open(template)
    except IOError as exc:
        raise AnsibleError(str(exc))
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(value)
    results = list()
    for item in fsm_results:
        results.append(dict(zip(re_table.header, item)))
    return results