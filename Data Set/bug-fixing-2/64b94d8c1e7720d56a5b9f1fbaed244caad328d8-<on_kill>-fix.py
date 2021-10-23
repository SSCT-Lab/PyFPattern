

def on_kill(self):
    super(BigQueryOperator, self).on_kill()
    if (self.bq_cursor is not None):
        self.log.info('Cancelling running query')
        self.bq_cursor.cancel_query()
