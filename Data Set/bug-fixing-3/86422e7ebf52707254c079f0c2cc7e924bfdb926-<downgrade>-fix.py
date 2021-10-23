def downgrade():
    op.drop_column('dag', 'schedule_interval')