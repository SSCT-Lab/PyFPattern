def test_set_private(self):
    group1 = self.create_group(checksum=('a' * 32))
    group2 = self.create_group(checksum=('b' * 32))
    for g in (group1, group2):
        GroupShare.objects.create(project_id=g.project_id, group=g)
        assert bool(g.get_share_id())
    self.login_as(user=self.user)
    response = self.get_valid_response(qs_params={
        'id': [group1.id, group2.id],
    }, isPublic='false')
    assert (response.data == {
        'isPublic': False,
    })
    new_group1 = Group.objects.get(id=group1.id)
    assert (not bool(new_group1.get_share_id()))
    new_group2 = Group.objects.get(id=group2.id)
    assert (not bool(new_group2.get_share_id()))