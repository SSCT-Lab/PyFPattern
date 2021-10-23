def get_vrf_description(vrf, module):
    command_type = 'cli_show_ascii'
    command = 'show run section vrf | begin ^vrf\\scontext\\s{0} | end ^vrf.*'.format(vrf)
    description = ''
    descr_regex = '.*description\\s(?P<descr>[\\S+\\s]+).*'
    body = execute_show_command(command, module, command_type)
    try:
        body = body[0]
        splitted_body = body.split('\n')
    except (AttributeError, IndexError):
        return description
    for element in splitted_body:
        if ('description' in element):
            match_description = re.match(descr_regex, element, re.DOTALL)
            group_description = match_description.groupdict()
            description = group_description['descr']
    return description