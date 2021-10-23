def forwards(self, orm):
    if is_postgres():
        db.execute('ALTER TABLE sentry_release ALTER COLUMN project_id DROP NOT NULL')
        db.execute('ALTER TABLE sentry_releasefile ALTER COLUMN project_id DROP NOT NULL')
    else:
        db.alter_column('sentry_release', 'project_id', self.gf('sentry.db.models.fields.bounded.BoundedPositiveIntegerField')(null=True))
        db.alter_column('sentry_releasefile', 'project_id', self.gf('sentry.db.models.fields.bounded.BoundedPositiveIntegerField')(null=True))