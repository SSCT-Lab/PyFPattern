

def test_cocoa_event(self):
    event = self.create_sample_event(platform='cocoa')
    group = event.group
    GroupShare.objects.create(project_id=group.project_id, group=group)
    self.browser.get('/share/issue/{}/'.format(group.get_share_id()))
    self.browser.wait_until('.entries')
    self.browser.snapshot('shared issue cocoa')
