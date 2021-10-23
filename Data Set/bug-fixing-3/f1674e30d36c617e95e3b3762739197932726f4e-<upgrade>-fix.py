def upgrade():
    '\n    Make TaskInstance.pool field not nullable.\n    '
    with create_session() as session:
        session.query(TaskInstance).filter(TaskInstance.pool.is_(None)).update({
            TaskInstance.pool: 'default_pool',
        }, synchronize_session=False)
        session.commit()
    conn = op.get_bind()
    if (conn.dialect.name == 'mssql'):
        op.drop_index('ti_pool', table_name='task_instance')
    with op.batch_alter_table('task_instance') as batch_op:
        batch_op.alter_column(column_name='pool', type_=sa.String(50), nullable=False)
    if (conn.dialect.name == 'mssql'):
        op.create_index('ti_pool', 'task_instance', ['pool', 'state', 'priority_weight'])