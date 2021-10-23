

def resetdb():
    '\n    Clear out the database\n    '
    from airflow import models
    from alembic.migration import MigrationContext
    log.info('Dropping tables that exist')
    connection = settings.engine.connect()
    models.base.Base.metadata.drop_all(connection)
    mc = MigrationContext.configure(connection)
    if mc._version.exists(connection):
        mc._version.drop(connection)
    from flask_appbuilder.models.sqla import Base
    Base.metadata.drop_all(connection)
    initdb()
