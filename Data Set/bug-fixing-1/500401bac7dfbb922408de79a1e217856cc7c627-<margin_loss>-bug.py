

def margin_loss(y_true, y_pred):
    (lamb, margin) = (0.5, 0.1)
    return ((y_true * K.square(K.relu(((1 - margin) - y_pred)))) + ((lamb * (1 - y_true)) * K.square(K.relu((y_pred - margin)))))
