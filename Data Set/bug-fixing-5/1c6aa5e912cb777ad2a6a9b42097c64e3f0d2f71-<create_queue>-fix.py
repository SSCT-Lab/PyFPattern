def create_queue(self, queue_name, attributes=None):
    '\n        Create queue using connection object\n\n        :param queue_name: name of the queue.\n        :type queue_name: str\n        :param attributes: additional attributes for the queue (default: None)\n            For details of the attributes parameter see :py:meth:`botocore.client.SQS.create_queue`\n        :type attributes: dict\n\n        :return: dict with the information about the queue\n            For details of the returned value see :py:meth:`botocore.client.SQS.create_queue`\n        :rtype: dict\n        '
    return self.get_conn().create_queue(QueueName=queue_name, Attributes=(attributes or {
        
    }))