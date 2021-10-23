

def does_volume_clone_exists(self):
    clone_obj = netapp_utils.zapi.NaElement('volume-clone-get')
    clone_obj.add_new_child('volume', self.volume)
    attributes_obj = netapp_utils.zapi.NaElement('desired-attributes')
    info_obj = netapp_utils.zapi.NaElement('volume-clone-info')
    clone_obj.add_child_elem(attributes_obj)
    attributes_obj.add_child_elem(info_obj)
    attributes_obj.add_new_child('volume', self.volume)
    attributes_obj.add_new_child('vserver', self.vserver)
    attributes_obj.add_new_child('parent-volume', self.parent_volume)
    try:
        self.server.invoke_successfully(clone_obj, True)
    except:
        return False
    return True
