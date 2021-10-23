

def forwards(self, orm):
    Project = orm['sentry.Project']
    ReleaseProject = orm['sentry.ReleaseProject']
    db.commit_transaction()
    queryset = Project.objects.all()
    for item in RangeQuerySetWrapperWithProgressBar(queryset):
        if (item.flags == (item.flags | 1)):
            continue
        if (not ReleaseProject.objects.filter(project=item).exists()):
            continue
        db.execute('UPDATE sentry_project SET flags = flags | 1 WHERE id = %s', [item.id])
    db.start_transaction()
