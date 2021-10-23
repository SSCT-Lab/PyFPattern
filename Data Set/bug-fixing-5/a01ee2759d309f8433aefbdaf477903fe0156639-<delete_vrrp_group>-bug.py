def delete_vrrp_group(self):
    'delete vrrp group attribute info'
    if self.is_vrrp_group_info_exist():
        conf_str = (CE_NC_SET_VRRP_GROUP_INFO_HEAD % (self.interface, self.vrid))
        if self.vrrp_type:
            vrrp_type = self.vrrp_type
            if (self.vrrp_type == 'admin'):
                vrrp_type = 'normal'
            if ((self.vrrp_type == 'member') and self.admin_vrid and self.admin_interface):
                vrrp_type = 'normal'
            conf_str += ('<vrrpType>%s</vrrpType>' % vrrp_type)
        if self.priority:
            if (self.priority == '100'):
                self.module.fail_json(msg='Error: The default value of priority is 100.')
            priority = '100'
            conf_str += ('<priority>%s</priority>' % priority)
        if self.fast_resume:
            fast_resume = 'false'
            if (self.fast_resume == 'enable'):
                fast_resume = 'true'
            conf_str += ('<fastResume>%s</fastResume>' % fast_resume)
        if self.advertise_interval:
            if (self.advertise_interval == '1000'):
                self.module.fail_json(msg='Error: The default value of advertise_interval is 1000.')
            advertise_interval = '1000'
            conf_str += ('<advertiseInterval>%s</advertiseInterval>' % advertise_interval)
        if self.preempt_timer_delay:
            if (self.preempt_timer_delay == '0'):
                self.module.fail_json(msg='Error: The default value of preempt_timer_delay is 0.')
            preempt_timer_delay = '0'
            conf_str += ('<delayTime>%s</delayTime>' % preempt_timer_delay)
        if self.holding_multiplier:
            if (self.holding_multiplier == '0'):
                self.module.fail_json(msg='Error: The default value of holding_multiplier is 3.')
            holding_multiplier = '3'
            conf_str += ('<holdMultiplier>%s</holdMultiplier>' % holding_multiplier)
        if self.auth_mode:
            auth_mode = self.auth_mode
            if ((self.auth_mode == 'md5') or (self.auth_mode == 'simple')):
                auth_mode = 'none'
            conf_str += ('<authenticationMode>%s</authenticationMode>' % auth_mode)
        conf_str += CE_NC_SET_VRRP_GROUP_INFO_TAIL
        recv_xml = set_nc_config(self.module, conf_str)
        if ('<ok/>' not in recv_xml):
            self.module.fail_json(msg='Error: set vrrp global atrribute info failed.')
        if (self.interface and self.vrid):
            if (self.vrrp_type == 'admin'):
                self.updates_cmd.append(('undo vrrp vrid %s admin' % self.vrid))
            if self.priority:
                self.updates_cmd.append(('interface %s' % self.interface))
                self.updates_cmd.append(('undo vrrp vrid %s priority' % self.vrid))
            if self.fast_resume:
                self.updates_cmd.append(('interface %s' % self.interface))
                self.updates_cmd.append(('undo vrrp vrid %s fast-resume' % self.vrid))
            if self.advertise_interval:
                self.updates_cmd.append(('interface %s' % self.interface))
                self.updates_cmd.append(('undo vrrp vrid %s timer advertise' % self.vrid))
            if self.preempt_timer_delay:
                self.updates_cmd.append(('interface %s' % self.interface))
                self.updates_cmd.append(('undo vrrp vrid %s preempt timer delay' % self.vrid))
            if self.holding_multiplier:
                self.updates_cmd.append(('interface %s' % self.interface))
                self.updates_cmd.append(('undo vrrp vrid %s holding-multiplier' % self.vrid))
            if (self.admin_vrid and self.admin_interface):
                self.updates_cmd.append(('interface %s' % self.interface))
                self.updates_cmd.append(('undo vrrp vrid %s track admin-vrrp' % self.vrid))
            if self.auth_mode:
                self.updates_cmd.append(('interface %s' % self.interface))
                self.updates_cmd.append(('undo vrrp vrid %s authentication-mode' % self.vrid))
            self.changed = True