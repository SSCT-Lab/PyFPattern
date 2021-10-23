def test_integration(self):
    Project.objects.all().delete()
    now = datetime(2016, 9, 12, tzinfo=pytz.utc)
    project = self.create_project(organization=self.organization, team=self.team, date_added=(now - timedelta(days=90)))
    tsdb.incr(tsdb.models.project, project.id, (now - timedelta(days=1)))
    member_set = set(project.team.member_set.all())
    with self.tasks():
        prepare_reports(timestamp=to_timestamp(now))
        assert (len(mail.outbox) == len(member_set) == 1)
        message = mail.outbox[0]
        assert (self.organization.name in message.subject)