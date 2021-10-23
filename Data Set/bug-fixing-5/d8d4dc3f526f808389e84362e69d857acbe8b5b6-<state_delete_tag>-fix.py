def state_delete_tag(self):
    '\n        Delete tag\n\n        '
    tag_id = self.global_tags[self.tag_name]['tag_id']
    self.tag_service.delete(tag_id=tag_id)
    self.module.exit_json(changed=True, results=dict(msg=("Tag '%s' deleted." % self.tag_name), tag_id=tag_id))