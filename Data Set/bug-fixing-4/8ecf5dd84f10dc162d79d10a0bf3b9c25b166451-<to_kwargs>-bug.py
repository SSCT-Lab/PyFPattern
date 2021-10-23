def to_kwargs(self, with_initializer=False):
    kwargs = {
        'name': self.name,
        'optimize_attr': {
            'learning_rate': self.learning_rate,
        },
        'regularizer': self.regularizer,
        'trainable': self.trainable,
        'gradient_clip_attr': self.gradient_clip,
        'model_average': self.model_average,
    }
    if with_initializer:
        kwargs['initializer'] = self.initializer
    return kwargs