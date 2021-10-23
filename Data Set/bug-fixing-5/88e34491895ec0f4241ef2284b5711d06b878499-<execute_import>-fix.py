def execute_import(self):
    ' used to import a role into Ansible Galaxy '
    colors = {
        'INFO': 'normal',
        'WARNING': C.COLOR_WARN,
        'ERROR': C.COLOR_ERROR,
        'SUCCESS': C.COLOR_OK,
        'FAILED': C.COLOR_ERROR,
    }
    github_user = to_text(context.CLIARGS['github_user'], errors='surrogate_or_strict')
    github_repo = to_text(context.CLIARGS['github_repo'], errors='surrogate_or_strict')
    if context.CLIARGS['check_status']:
        task = self.api.get_import_task(github_user=github_user, github_repo=github_repo)
    else:
        task = self.api.create_import_task(github_user, github_repo, reference=context.CLIARGS['reference'], role_name=context.CLIARGS['role_name'])
        if (len(task) > 1):
            display.display(('WARNING: More than one Galaxy role associated with Github repo %s/%s.' % (github_user, github_repo)), color='yellow')
            display.display(('The following Galaxy roles are being updated:' + '\n'), color=C.COLOR_CHANGED)
            for t in task:
                display.display(('%s.%s' % (t['summary_fields']['role']['namespace'], t['summary_fields']['role']['name'])), color=C.COLOR_CHANGED)
            display.display(('\nTo properly namespace this role, remove each of the above and re-import %s/%s from scratch' % (github_user, github_repo)), color=C.COLOR_CHANGED)
            return 0
        display.display(('Successfully submitted import request %d' % task[0]['id']))
        if (not context.CLIARGS['wait']):
            display.display(('Role name: %s' % task[0]['summary_fields']['role']['name']))
            display.display(('Repo: %s/%s' % (task[0]['github_user'], task[0]['github_repo'])))
    if (context.CLIARGS['check_status'] or context.CLIARGS['wait']):
        msg_list = []
        finished = False
        while (not finished):
            task = self.api.get_import_task(task_id=task[0]['id'])
            for msg in task[0]['summary_fields']['task_messages']:
                if (msg['id'] not in msg_list):
                    display.display(msg['message_text'], color=colors[msg['message_type']])
                    msg_list.append(msg['id'])
            if (task[0]['state'] in ['SUCCESS', 'FAILED']):
                finished = True
            else:
                time.sleep(10)
    return 0