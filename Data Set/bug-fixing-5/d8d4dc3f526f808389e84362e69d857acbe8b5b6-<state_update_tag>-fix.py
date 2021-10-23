def state_update_tag(self):
    '\n        Update tag\n\n        '
    changed = False
    results = dict(msg=('Tag %s is unchanged.' % self.tag_name), tag_id=self.global_tags[self.tag_name]['tag_id'])
    tag_update_spec = self.tag_service.UpdateSpec()
    tag_desc = self.global_tags[self.tag_name]['tag_description']
    desired_tag_desc = self.params.get('tag_description')
    if (tag_desc != desired_tag_desc):
        tag_update_spec.setDescription = desired_tag_desc
        results['msg'] = ('Tag %s updated.' % self.tag_name)
        changed = True
    self.module.exit_json(changed=changed, results=results)