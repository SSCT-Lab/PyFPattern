def record_event(self, event):
    self.publisher.publish(self.topic, data=dumps(event.serialize()))