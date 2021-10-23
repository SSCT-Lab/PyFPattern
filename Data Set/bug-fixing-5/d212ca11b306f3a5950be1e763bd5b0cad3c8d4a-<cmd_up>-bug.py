def cmd_up(self):
    start_deps = self.dependencies
    service_names = self.services
    detached = True
    result = dict(changed=False, actions=[], ansible_facts=dict())
    up_options = {
        '--no-recreate': False,
        '--build': True,
        '--no-build': False,
        '--no-deps': False,
        '--force-recreate': False,
    }
    if (self.recreate == 'never'):
        up_options['--no-recreate'] = True
    elif (self.recreate == 'always'):
        up_options['--force-recreate'] = True
    if self.remove_orphans:
        up_options['--remove-orphans'] = True
    converge = convergence_strategy_from_opts(up_options)
    self.log(('convergence strategy: %s' % converge))
    if self.pull:
        pull_output = self.cmd_pull()
        result['changed'] = pull_output['changed']
        result['actions'] += pull_output['actions']
    if self.build:
        build_output = self.cmd_build()
        result['changed'] = build_output['changed']
        result['actions'] += build_output['actions']
    for service in self.project.services:
        if ((not service_names) or (service.name in service_names)):
            plan = service.convergence_plan(strategy=converge)
            if (plan.action != 'noop'):
                result['changed'] = True
                result_action = dict(service=service.name)
                result_action[plan.action] = []
                for container in plan.containers:
                    result_action[plan.action].append(dict(id=container.id, name=container.name, short_id=container.short_id))
                result['actions'].append(result_action)
    if ((not self.check_mode) and result['changed']):
        (out_redir_name, err_redir_name) = make_redirection_tempfiles()
        try:
            with stdout_redirector(out_redir_name):
                with stderr_redirector(err_redir_name):
                    do_build = build_action_from_opts(up_options)
                    self.log(('Setting do_build to %s' % do_build))
                    self.project.up(service_names=service_names, start_deps=start_deps, strategy=converge, do_build=do_build, detached=detached, remove_orphans=self.remove_orphans, timeout=self.timeout)
        except Exception as exc:
            fail_reason = get_failure_info(exc, out_redir_name, err_redir_name, msg_format='Error starting project %s')
            self.client.module.fail_json(**fail_reason)
        else:
            cleanup_redirection_tempfiles(out_redir_name, err_redir_name)
    if self.stopped:
        stop_output = self.cmd_stop(service_names)
        result['changed'] = stop_output['changed']
        result['actions'] += stop_output['actions']
    if self.restarted:
        restart_output = self.cmd_restart(service_names)
        result['changed'] = restart_output['changed']
        result['actions'] += restart_output['actions']
    if self.scale:
        scale_output = self.cmd_scale()
        result['changed'] = scale_output['changed']
        result['actions'] += scale_output['actions']
    for service in self.project.services:
        result['ansible_facts'][service.name] = dict()
        for container in service.containers(stopped=True):
            inspection = container.inspect()
            facts = dict(cmd=[], labels=dict(), image=None, state=dict(running=None, status=None), networks=dict())
            if (inspection['Config'].get('Cmd', None) is not None):
                facts['cmd'] = inspection['Config']['Cmd']
            if (inspection['Config'].get('Labels', None) is not None):
                facts['labels'] = inspection['Config']['Labels']
            if (inspection['Config'].get('Image', None) is not None):
                facts['image'] = inspection['Config']['Image']
            if (inspection['State'].get('Running', None) is not None):
                facts['state']['running'] = inspection['State']['Running']
            if (inspection['State'].get('Status', None) is not None):
                facts['state']['status'] = inspection['State']['Status']
            if (inspection.get('NetworkSettings') and inspection['NetworkSettings'].get('Networks')):
                networks = inspection['NetworkSettings']['Networks']
                for key in networks:
                    facts['networks'][key] = dict(aliases=[], globalIPv6=None, globalIPv6PrefixLen=0, IPAddress=None, IPPrefixLen=0, links=None, macAddress=None)
                    if (networks[key].get('Aliases', None) is not None):
                        facts['networks'][key]['aliases'] = networks[key]['Aliases']
                    if (networks[key].get('GlobalIPv6Address', None) is not None):
                        facts['networks'][key]['globalIPv6'] = networks[key]['GlobalIPv6Address']
                    if (networks[key].get('GlobalIPv6PrefixLen', None) is not None):
                        facts['networks'][key]['globalIPv6PrefixLen'] = networks[key]['GlobalIPv6PrefixLen']
                    if (networks[key].get('IPAddress', None) is not None):
                        facts['networks'][key]['IPAddress'] = networks[key]['IPAddress']
                    if (networks[key].get('IPPrefixLen', None) is not None):
                        facts['networks'][key]['IPPrefixLen'] = networks[key]['IPPrefixLen']
                    if (networks[key].get('Links', None) is not None):
                        facts['networks'][key]['links'] = networks[key]['Links']
                    if (networks[key].get('MacAddress', None) is not None):
                        facts['networks'][key]['macAddress'] = networks[key]['MacAddress']
            result['ansible_facts'][service.name][container.name] = facts
    return result