def forwards(self, orm):
    db.alter_column('sentry_release', 'project_id', self.gf('sentry.db.models.fields.bounded.BoundedPositiveIntegerField')(null=True))
    db.alter_column('sentry_releasefile', 'project_id', self.gf('sentry.db.models.fields.bounded.BoundedPositiveIntegerField')(null=True))