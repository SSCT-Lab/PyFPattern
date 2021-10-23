def contrastive_loss(y_true, y_pred):
    "Contrastive loss from Hadsell-et-al.'06\n    http://yann.lecun.com/exdb/publis/pdf/hadsell-chopra-lecun-06.pdf\n    "
    margin = 1
    sqaure_pred = K.square(y_pred)
    margin_square = K.square(K.maximum((margin - y_pred), 0))
    return K.mean(((y_true * sqaure_pred) + ((1 - y_true) * margin_square)))