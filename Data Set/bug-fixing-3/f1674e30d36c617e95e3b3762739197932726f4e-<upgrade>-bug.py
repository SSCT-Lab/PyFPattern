def upgrade():
    '\n    Make TaskInstance.pool field not nullable.\n    '
    with create_session() as session:
        session.query(TaskInstance).filter(TaskInstance.pool.is_(None)).update({
            TaskInstance.pool: 'default_pool',
        }, synchronize_session=False)
        session.commit()
    with op.batch_alter_table('task_instance') as batch_op:
        batch_op.alter_column(column_name='pool', type_=sa.String(50), nullable=False)