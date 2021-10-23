def record_event(self, event):
    if (self.publisher is not None):
        self.publisher.publish(self.topic, data=dumps(event.serialize()))