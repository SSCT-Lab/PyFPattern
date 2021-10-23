

def __init__(self, module):
    '\n        Constructor\n        '
    super(VmwareTagManager, self).__init__(module)
    self.pyv = PyVmomi(module=module)
    self.object_type = self.params.get('object_type')
    self.object_name = self.params.get('object_name')
    self.managed_object = None
    if (self.object_type == 'VirtualMachine'):
        self.managed_object = self.pyv.get_vm_or_template(self.object_name)
    if (self.managed_object is None):
        self.module.fail_json(msg=('Failed to find the managed object for %s with type %s' % (self.object_name, self.object_type)))
    if (not hasattr(self.managed_object, '_moId')):
        self.module.fail_json(msg=('Unable to find managed object id for %s managed object' % self.object_name))
    self.dynamic_managed_object = DynamicID(type=self.object_type, id=self.managed_object._moId)
    self.tag_service = Tag(self.connect)
    self.category_service = Category(self.connect)
    self.tag_association_svc = TagAssociation(self.connect)
    self.tag_names = self.params.get('tag_names')
