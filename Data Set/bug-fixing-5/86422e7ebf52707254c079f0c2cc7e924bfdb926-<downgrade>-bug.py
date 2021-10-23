def downgrade():
    op.drop_column('dag', sa.Column('schedule_interval', sa.Text(), nullable=True))