

def to_kwargs(self, with_initializer=False):
    kwargs = {
        'name': self.name,
        'learning_rate': self.learning_rate,
        'regularizer': self.regularizer,
        'trainable': self.trainable,
        'clip_attr': self.clip,
    }
    if with_initializer:
        kwargs['initializer'] = self.initializer
    return kwargs
