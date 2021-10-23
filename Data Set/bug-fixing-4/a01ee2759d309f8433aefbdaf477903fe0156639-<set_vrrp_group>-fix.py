def set_vrrp_group(self):
    'set vrrp group attribute info'
    if self.is_vrrp_group_info_change():
        conf_str = (CE_NC_SET_VRRP_GROUP_INFO_HEAD % (self.interface, self.vrid))
        if self.vrrp_type:
            conf_str += ('<vrrpType>%s</vrrpType>' % self.vrrp_type)
        if self.admin_vrid:
            conf_str += ('<adminVrrpId>%s</adminVrrpId>' % self.admin_vrid)
        if self.admin_interface:
            conf_str += ('<adminIfName>%s</adminIfName>' % self.admin_interface)
            if self.admin_flowdown:
                conf_str += ('<unflowdown>%s</unflowdown>' % self.admin_flowdown)
        if self.priority:
            conf_str += ('<priority>%s</priority>' % self.priority)
        if (self.vrrp_type == 'admin'):
            if self.admin_ignore_if_down:
                conf_str += ('<adminIgnoreIfDown>%s</adminIgnoreIfDown>' % self.admin_ignore_if_down)
        if self.fast_resume:
            fast_resume = 'false'
            if (self.fast_resume == 'enable'):
                fast_resume = 'true'
            conf_str += ('<fastResume>%s</fastResume>' % fast_resume)
        if self.advertise_interval:
            conf_str += ('<advertiseInterval>%s</advertiseInterval>' % self.advertise_interval)
        if self.preempt_timer_delay:
            conf_str += ('<delayTime>%s</delayTime>' % self.preempt_timer_delay)
        if self.holding_multiplier:
            conf_str += ('<holdMultiplier>%s</holdMultiplier>' % self.holding_multiplier)
        if self.auth_mode:
            conf_str += ('<authenticationMode>%s</authenticationMode>' % self.auth_mode)
        if self.auth_key:
            conf_str += ('<authenticationKey>%s</authenticationKey>' % self.auth_key)
        if (self.auth_mode == 'simple'):
            conf_str += ('<isPlain>%s</isPlain>' % self.is_plain)
        conf_str += CE_NC_SET_VRRP_GROUP_INFO_TAIL
        recv_xml = set_nc_config(self.module, conf_str)
        if ('<ok/>' not in recv_xml):
            self.module.fail_json(msg='Error: set vrrp group atrribute info failed.')
        if (self.interface and self.vrid):
            self.updates_cmd.append(('interface %s' % self.interface))
            if (self.vrrp_type == 'admin'):
                if (self.admin_ignore_if_down == 'true'):
                    self.updates_cmd.append(('vrrp vrid %s admin ignore-if-down' % self.vrid))
                else:
                    self.updates_cmd.append(('vrrp vrid %s admin' % self.vrid))
            if self.priority:
                self.updates_cmd.append(('vrrp vrid %s priority %s' % (self.vrid, self.priority)))
            if (self.fast_resume == 'enable'):
                self.updates_cmd.append(('vrrp vrid %s fast-resume' % self.vrid))
            if (self.fast_resume == 'disable'):
                self.updates_cmd.append(('undo vrrp vrid %s fast-resume' % self.vrid))
            if self.advertise_interval:
                advertise_interval = (int(self.advertise_interval) / 1000)
                self.updates_cmd.append(('vrrp vrid %s timer advertise %s<seconds>' % (self.vrid, int(advertise_interval))))
            if self.preempt_timer_delay:
                self.updates_cmd.append(('vrrp vrid %s preempt timer delay %s' % (self.vrid, self.preempt_timer_delay)))
            if self.holding_multiplier:
                self.updates_cmd.append(('vrrp vrid %s holding-multiplier %s' % (self.vrid, self.holding_multiplier)))
            if (self.admin_vrid and self.admin_interface):
                if (self.admin_flowdown == 'true'):
                    self.updates_cmd.append(('vrrp vrid %s track admin-vrrp interface %s vrid %s unflowdown' % (self.vrid, self.admin_interface, self.admin_vrid)))
                else:
                    self.updates_cmd.append(('vrrp vrid %s track admin-vrrp interface %s vrid %s' % (self.vrid, self.admin_interface, self.admin_vrid)))
            if (self.auth_mode and self.auth_key):
                if (self.auth_mode == 'simple'):
                    if (self.is_plain == 'true'):
                        self.updates_cmd.append(('vrrp vrid %s authentication-mode simple plain %s' % (self.vrid, self.auth_key)))
                    else:
                        self.updates_cmd.append(('vrrp vrid %s authentication-mode simple cipher %s' % (self.vrid, self.auth_key)))
                if (self.auth_mode == 'md5'):
                    self.updates_cmd.append(('vrrp vrid %s authentication-mode md5 %s' % (self.vrid, self.auth_key)))
            self.changed = True