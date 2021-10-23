def core(module):
    do_manager = DoManager(module)
    state = module.params.get('state')
    domain = do_manager.find()
    if (state == 'present'):
        if (not domain):
            domain = do_manager.add()
            if ('message' in domain):
                module.fail_json(changed=False, msg=domain['message'])
            else:
                module.exit_json(changed=True, domain=domain)
        else:
            records = do_manager.all_domain_records()
            at_record = None
            for record in records['domain_records']:
                if ((record['name'] == '@') and (record['type'] == 'A')):
                    at_record = record
            if (not (at_record['data'] == module.params.get('ip'))):
                do_manager.edit_domain_record()
                module.exit_json(changed=True, domain=do_manager.find())
            else:
                module.exit_json(changed=False, domain=do_manager.domain_record())
    elif (state == 'absent'):
        if (not domain):
            module.exit_json(changed=False, msg='Domain not found')
        else:
            delete_event = do_manager.destroy_domain()
            if (not delete_event):
                module.fail_json(changed=False, msg=delete_event['message'])
            else:
                module.exit_json(changed=True, event=None)
        delete_event = do_manager.destroy_domain()
        module.exit_json(changed=delete_event)