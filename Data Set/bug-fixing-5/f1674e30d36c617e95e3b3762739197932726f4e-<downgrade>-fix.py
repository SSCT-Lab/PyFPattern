def downgrade():
    '\n    Make TaskInstance.pool field nullable.\n    '
    conn = op.get_bind()
    if (conn.dialect.name == 'mssql'):
        op.drop_index('ti_pool', table_name='task_instance')
    with op.batch_alter_table('task_instance') as batch_op:
        batch_op.alter_column(column_name='pool', type_=sa.String(50), nullable=True)
    if (conn.dialect.name == 'mssql'):
        op.create_index('ti_pool', 'task_instance', ['pool', 'state', 'priority_weight'])
    with create_session() as session:
        session.query(TaskInstance).filter((TaskInstance.pool == 'default_pool')).update({
            TaskInstance.pool: None,
        }, synchronize_session=False)
        session.commit()