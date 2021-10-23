def apply(self):
    'Call create/modify/delete operations'
    changed = False
    volume_exists = False
    rename_volume = False
    resize_volume = False
    move_volume = False
    modify_volume = False
    state_change = False
    volume_detail = self.get_volume()
    if volume_detail:
        volume_exists = True
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if ((self.aggregate_name is not None) and (volume_detail['aggregate_name'] != self.aggregate_name)):
                move_volume = True
                changed = True
            if ((self.size is not None) and (str(volume_detail['size']) != str(self.size))):
                resize_volume = True
                changed = True
            if ((volume_detail['is_online'] is not None) and (volume_detail['is_online'] != self.is_online)):
                state_change = True
                changed = True
            if ((self.new_name is not None) and (self.name != self.new_name)):
                rename_volume = True
                changed = True
            if ((self.policy is not None) and (self.policy != volume_detail['policy'])):
                modify_volume = True
                changed = True
            if ((self.space_guarantee is not None) and (self.space_guarantee != volume_detail['space_guarantee'])):
                modify_volume = True
                changed = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not volume_exists):
                self.create_volume()
            else:
                if resize_volume:
                    self.resize_volume()
                if state_change:
                    self.change_volume_state()
                if modify_volume:
                    self.volume_modify()
                if rename_volume:
                    self.rename_volume()
                if move_volume:
                    self.move_volume()
        elif (self.state == 'absent'):
            self.delete_volume()
    self.module.exit_json(changed=changed)