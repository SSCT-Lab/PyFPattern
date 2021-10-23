

def set_host_configuration_facts(self):
    changed = False
    for host in self.hosts:
        option_manager = host.configManager.advancedOption
        host_facts = {
            
        }
        for option in option_manager.QueryOptions():
            host_facts[option.key] = dict(value=option.value)
        for s_option in option_manager.supportedOption:
            host_facts[s_option.key].update(option_type=s_option.optionType)
        change_option_list = []
        for (option_key, option_value) in self.options.items():
            if (option_key in host_facts):
                if ('option_type' in host_facts[option_key]):
                    option_type = host_facts[option_key]['option_type']
                    if (self.is_boolean(option_value) and isinstance(option_type, vim.option.BoolOption)):
                        option_value = self.is_truthy(option_value)
                    elif ((isinstance(option_value, integer_types) or self.is_integer(option_value)) and isinstance(option_type, vim.option.IntOption)):
                        option_value = VmomiSupport.vmodlTypes['int'](option_value)
                    elif ((isinstance(option_value, integer_types) or self.is_integer(option_value, 'long')) and isinstance(option_type, vim.option.LongOption)):
                        option_value = VmomiSupport.vmodlTypes['long'](option_value)
                    elif (isinstance(option_value, float) and isinstance(option_type, vim.option.FloatOption)):
                        pass
                    elif (isinstance(option_value, string_types) and isinstance(option_type, (vim.option.StringOption, vim.option.ChoiceOption))):
                        pass
                    else:
                        self.module.fail_json(msg=('Provided value is of type %s. Option %s expects: %s' % (type(option_value), option_key, type(option_type))))
                else:
                    self.module.fail_json(msg=('Cannot change read only option %s to %s.' % (option_key, option_value)))
                if (option_value != host_facts[option_key]['value']):
                    change_option_list.append(vim.option.OptionValue(key=option_key, value=option_value))
                    changed = True
            else:
                self.module.fail_json(msg=('Unknown option %s' % option_key))
        if changed:
            try:
                option_manager.UpdateOptions(changedValue=change_option_list)
            except (vmodl.fault.SystemError, vmodl.fault.InvalidArgument) as e:
                self.module.fail_json(msg=('Failed to update option/s as one or more OptionValue contains an invalid value: %s' % to_native(e.msg)))
            except vim.fault.InvalidName as e:
                self.module.fail_json(msg=('Failed to update option/s as one or more OptionValue objects refers to a non-existent option : %s' % to_native(e.msg)))
    self.module.exit_json(changed=changed)
