def __init__(self, module):
    super(VmwareTag, self).__init__(module)
    self.tag_service = Tag(self.connect)
    self.global_tags = dict()
    self.tag_name = self.params.get('tag_name')
    self.get_all_tags()
    self.category_service = Category(self.connect)