@apply_defaults
def __init__(self, query_execution_id, max_retires=None, aws_conn_id='aws_default', sleep_time=10, *args, **kwargs):
    super(AthenaSensor, self).__init__(*args, **kwargs)
    self.aws_conn_id = aws_conn_id
    self.query_execution_id = query_execution_id
    self.hook = None
    self.sleep_time = sleep_time
    self.max_retires = max_retires