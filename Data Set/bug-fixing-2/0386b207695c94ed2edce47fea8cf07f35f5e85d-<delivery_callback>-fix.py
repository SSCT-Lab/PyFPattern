

def delivery_callback(self, error, message):
    if (error is not None):
        logger.warning('Could not publish event (error: %s): %r', error, message)
