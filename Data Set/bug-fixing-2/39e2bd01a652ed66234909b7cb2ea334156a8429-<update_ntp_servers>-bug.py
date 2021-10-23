

def update_ntp_servers(self, host, ntp_servers, operation='add'):
    changed = False
    host_date_time_manager = host.configManager.dateTimeSystem
    if host_date_time_manager:
        available_ntp_servers = host_date_time_manager.dateTimeInfo.ntpConfig.server
        if (operation == 'add'):
            available_ntp_servers = (available_ntp_servers + ntp_servers)
        elif (operation == 'delete'):
            for server in ntp_servers:
                if (server in available_ntp_servers):
                    available_ntp_servers.remove(server)
        ntp_config_spec = vim.host.NtpConfig()
        ntp_config_spec.server = available_ntp_servers
        date_config_spec = vim.host.DateTimeConfig()
        date_config_spec.ntpConfig = ntp_config_spec
        try:
            host_date_time_manager.UpdateDateTimeConfig(date_config_spec)
            self.results[host.name]['after_change_ntp_servers'] = host_date_time_manager.dateTimeInfo.ntpConfig.server
            changed = True
        except vim.fault.HostConfigFault as e:
            self.results[host.name]['error'] = to_native(e.msg)
        except Exception as e:
            self.results[host.name]['error'] = to_native(e)
    return changed
