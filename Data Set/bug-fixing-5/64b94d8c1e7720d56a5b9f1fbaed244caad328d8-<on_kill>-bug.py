def on_kill(self):
    super(BigQueryOperator, self).on_kill()
    if (self.bq_cursor is not None):
        self.log.info('Canceling running query due to execution timeout')
        self.bq_cursor.cancel_query()