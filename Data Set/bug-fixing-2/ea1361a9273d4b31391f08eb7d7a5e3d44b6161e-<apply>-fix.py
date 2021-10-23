

def apply(self):
    property_changed = False
    multiple_properties_changed = False
    size_changed = False
    lun_exists = False
    lun_detail = self.get_lun()
    if lun_detail:
        lun_exists = True
        current_size = lun_detail['size']
        if (self.state == 'absent'):
            property_changed = True
        elif (self.state == 'present'):
            if (not (int(current_size) == self.size)):
                size_changed = True
                property_changed = True
    elif (self.state == 'present'):
        property_changed = True
    if property_changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not lun_exists):
                self.create_lun()
            elif size_changed:
                size_changed = self.resize_lun()
                if ((not size_changed) and (not multiple_properties_changed)):
                    property_changed = False
        elif (self.state == 'absent'):
            self.delete_lun()
    changed = (property_changed or size_changed)
    self.module.exit_json(changed=changed)
