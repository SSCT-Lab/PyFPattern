def create_queue(self, queue_name, attributes=None):
    return self.get_conn().create_queue(QueueName=queue_name, Attributes=(attributes or {
        
    }))