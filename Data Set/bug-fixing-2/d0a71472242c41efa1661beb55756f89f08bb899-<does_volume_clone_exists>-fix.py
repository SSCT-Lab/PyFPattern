

def does_volume_clone_exists(self):
    clone_obj = netapp_utils.zapi.NaElement('volume-clone-get')
    clone_obj.add_new_child('volume', self.volume)
    try:
        results = self.server.invoke_successfully(clone_obj, True)
    except:
        return False
    attributes = results.get_child_by_name('attributes')
    info = attributes.get_child_by_name('volume-clone-info')
    parent_volume = info.get_child_content('parent-volume')
    if (parent_volume == self.parent_volume):
        return True
    self.module.fail_json(msg=('Error clone %s already exists for parent %s' % (self.volume, parent_volume)))
