def write_batch_data(self, items):
    '\n        Write batch items to DynamoDB table with provisioned throughout capacity.\n        '
    dynamodb_conn = self.get_conn()
    try:
        table = dynamodb_conn.Table(self.table_name)
        with table.batch_writer(overwrite_by_pkeys=self.table_keys) as batch:
            for item in items:
                batch.put_item(Item=item)
        return True
    except Exception as general_error:
        raise AirflowException('Failed to insert items in dynamodb, error: {error}'.format(error=str(general_error)))