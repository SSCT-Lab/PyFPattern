def get_igmp_snooping(module):
    command = 'show run all | include igmp.snooping'
    existing = {
        
    }
    body = execute_show_command(command, module)[0]
    if body:
        split_body = body.splitlines()
        if ('no ip igmp snooping' in split_body):
            existing['snooping'] = False
        else:
            existing['snooping'] = True
        if ('no ip igmp snooping report-suppression' in split_body):
            existing['report_supp'] = False
        elif ('ip igmp snooping report-suppression' in split_body):
            existing['report_supp'] = True
        if ('no ip igmp snooping link-local-groups-suppression' in split_body):
            existing['link_local_grp_supp'] = False
        elif ('ip igmp snooping link-local-groups-suppression' in split_body):
            existing['link_local_grp_supp'] = True
        if ('ip igmp snooping v3-report-suppression' in split_body):
            existing['v3_report_supp'] = True
        else:
            existing['v3_report_supp'] = False
        existing['group_timeout'] = get_group_timeout(body)
    return existing