def _send(self, project_id, _type, extra_data=(), asynchronous=True):
    self.producer.poll(0.0)
    assert isinstance(extra_data, tuple)
    key = six.text_type(project_id)
    try:
        self.producer.produce(self.publish_topic, key=key.encode('utf-8'), value=json.dumps(((EVENT_PROTOCOL_VERSION, _type) + extra_data)), on_delivery=self.delivery_callback)
    except Exception as error:
        logger.error('Could not publish message: %s', error, exc_info=True)
        return
    if (not asynchronous):
        self.producer.flush()