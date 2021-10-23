def set_host_configuration_facts(self):
    changed = False
    for host in self.hosts:
        option_manager = host.configManager.advancedOption
        host_facts = {
            
        }
        for option in option_manager.QueryOptions():
            host_facts[option.key] = option.value
        change_option_list = []
        for (option_key, option_value) in self.options.items():
            if ((option_key in host_facts) and (option_value != host_facts[option_key])):
                change_option_list.append(vim.option.OptionValue(key=option_key, value=option_value))
                changed = True
        if changed:
            try:
                option_manager.UpdateOptions(changedValue=change_option_list)
            except vmodl.fault.InvalidArgument as e:
                self.module.fail_json(msg=('Failed to update option/s as one or more OptionValue contains an invalid value: %s' % to_native(e.msg)))
            except vim.fault.InvalidName as e:
                self.module.fail_json(msg=('Failed to update option/s as one or more OptionValue objects refers to a non-existent option : %s' % to_native(e.msg)))
    self.module.exit_json(changed=changed)