

def classifer_metrics(label, pred):
    '\n    computes f1, precision and recall on the entity class\n    '
    prediction = np.argmax(pred, axis=1)
    label = label.astype(int)
    pred_is_entity = (prediction != not_entity_index)
    label_is_entity = (label != not_entity_index)
    corr_pred = ((prediction == label) == (pred_is_entity == True))
    num_entities = np.sum(label_is_entity)
    entity_preds = np.sum(pred_is_entity)
    correct_entitites = np.sum(corr_pred[pred_is_entity])
    if (entity_preds == 0):
        precision = np.nan
    else:
        precision = (correct_entitites / entity_preds)
    recall = (correct_entitites / num_entities)
    if (num_entities == 0):
        recall = np.nan
    if ((precision + recall) == 0):
        f1 = 0
    else:
        f1 = (((2 * precision) * recall) / (precision + recall))
    return (precision, recall, f1)
