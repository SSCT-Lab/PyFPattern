def send_message(self, queue_url, message_body, delay_seconds=0, message_attributes=None):
    return self.get_conn().send_message(QueueUrl=queue_url, MessageBody=message_body, DelaySeconds=delay_seconds, MessageAttributes=(message_attributes or {
        
    }))