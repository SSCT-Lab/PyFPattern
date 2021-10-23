def downgrade():
    '\n    Make TaskInstance.pool field nullable.\n    '
    with op.batch_alter_table('task_instance') as batch_op:
        batch_op.alter_column(column_name='pool', type_=sa.String(50), nullable=True)
    with create_session() as session:
        session.query(TaskInstance).filter((TaskInstance.pool == 'default_pool')).update({
            TaskInstance.pool: None,
        }, synchronize_session=False)
        session.commit()