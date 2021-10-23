def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    if ('known_event' in inspector.get_table_names()):
        op.drop_constraint('known_event_user_id_fkey', 'known_event')
    op.drop_table('chart')
    op.drop_table('users')