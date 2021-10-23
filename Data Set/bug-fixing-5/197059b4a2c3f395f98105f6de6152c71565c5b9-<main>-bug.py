def main():
    result = {
        
    }
    resource = {
        
    }
    category_list = []
    module = AnsibleModule(argument_spec=dict(category=dict(type='list', default=['Systems']), command=dict(type='list'), baseuri=dict(required=True), user=dict(required=True), password=dict(required=True, no_log=True)), supports_check_mode=False)
    creds = {
        'user': module.params['user'],
        'pswd': module.params['password'],
    }
    root_uri = ('https://' + module.params['baseuri'])
    rf_uri = '/redfish/v1'
    rf_utils = RedfishUtils(creds, root_uri)
    if ('all' in module.params['category']):
        for entry in CATEGORY_COMMANDS_ALL:
            category_list.append(entry)
    else:
        category_list = module.params['category']
    for category in category_list:
        command_list = []
        if (category in CATEGORY_COMMANDS_ALL):
            if (not module.params['command']):
                command_list.append(CATEGORY_COMMANDS_DEFAULT[category])
            elif ('all' in module.params['command']):
                for entry in range(len(CATEGORY_COMMANDS_ALL[category])):
                    command_list.append(CATEGORY_COMMANDS_ALL[category][entry])
            else:
                command_list = module.params['command']
                for cmd in command_list:
                    if (cmd not in CATEGORY_COMMANDS_ALL[category]):
                        module.fail_json(msg=('Invalid Command: %s' % cmd))
        else:
            module.fail_json(msg=('Invalid Category: %s' % category))
        if (category == 'Systems'):
            resource = rf_utils._find_systems_resource(rf_uri)
            if (resource['ret'] is False):
                module.fail_json(msg=resource['msg'])
            for command in command_list:
                if (command == 'GetSystemInventory'):
                    result['system'] = rf_utils.get_system_inventory()
                elif (command == 'GetPsuInventory'):
                    result['psu'] = rf_utils.get_psu_inventory()
                elif (command == 'GetCpuInventory'):
                    result['cpu'] = rf_utils.get_cpu_inventory()
                elif (command == 'GetNicInventory'):
                    result['nic'] = rf_utils.get_nic_inventory()
                elif (command == 'GetStorageControllerInventory'):
                    result['storage_controller'] = rf_utils.get_storage_controller_inventory()
                elif (command == 'GetDiskInventory'):
                    result['disk'] = rf_utils.get_disk_inventory()
                elif (command == 'GetBiosAttributes'):
                    result['bios_attribute'] = rf_utils.get_bios_attributes()
                elif (command == 'GetBiosBootOrder'):
                    result['bios_boot_order'] = rf_utils.get_bios_boot_order()
        elif (category == 'Chassis'):
            resource = rf_utils._find_chassis_resource(rf_uri)
            if (resource['ret'] is False):
                module.fail_json(msg=resource['msg'])
            for command in command_list:
                if (command == 'GetFanInventory'):
                    result['fan'] = rf_utils.get_fan_inventory()
        elif (category == 'Accounts'):
            resource = rf_utils._find_accountservice_resource(rf_uri)
            if (resource['ret'] is False):
                module.fail_json(msg=resource['msg'])
            for command in command_list:
                if (command == 'ListUsers'):
                    result['user'] = rf_utils.list_users()
        elif (category == 'Update'):
            resource = rf_utils._find_updateservice_resource(rf_uri)
            if (resource['ret'] is False):
                module.fail_json(msg=resource['msg'])
            for command in command_list:
                if (command == 'GetFirmwareInventory'):
                    result['firmware'] = rf_utils.get_firmware_inventory()
        elif (category == 'Manager'):
            resource = rf_utils._find_managers_resource(rf_uri)
            if (resource['ret'] is False):
                module.fail_json(msg=resource['msg'])
            for command in command_list:
                if (command == 'GetManagerAttributes'):
                    result['manager_attributes'] = rf_utils.get_manager_attributes()
                elif (command == 'GetLogs'):
                    result['log'] = rf_utils.get_logs()
    module.exit_json(ansible_facts=dict(redfish_facts=result))