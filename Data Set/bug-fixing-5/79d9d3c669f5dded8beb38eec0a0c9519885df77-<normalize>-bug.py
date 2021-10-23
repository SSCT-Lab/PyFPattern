def normalize(x):
    return (x / (K.sqrt(K.mean(K.square(x))) + K.epsilon()))