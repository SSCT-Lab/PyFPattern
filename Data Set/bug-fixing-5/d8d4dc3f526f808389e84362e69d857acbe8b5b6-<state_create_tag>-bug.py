def state_create_tag(self):
    '\n        Function to create tag\n\n        '
    tag_spec = self.tag_service.CreateSpec()
    tag_spec.name = self.tag_name
    tag_spec.description = self.params.get('tag_description')
    category_id = self.params.get('category_id', None)
    if (category_id is None):
        self.module.fail_json(msg="'category_id' is required parameter while creating tag.")
    tag_spec.category_id = category_id
    tag_id = self.tag_service.create(tag_spec)
    if tag_id:
        self.module.exit_json(changed=True, results=dict(msg=("Tag '%s' created." % tag_spec.name), tag_id=tag_id))
    self.module.exit_json(changed=False, results=dict(msg='No tag created', tag_id=''))