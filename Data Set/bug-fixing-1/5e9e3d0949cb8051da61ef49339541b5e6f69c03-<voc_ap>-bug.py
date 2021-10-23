

def voc_ap(rec, prec, use_07_metric=False):
    '\n    average precision calculations\n    [precision integrated to recall]\n    :param rec: recall\n    :param prec: precision\n    :param use_07_metric: 2007 metric is 11-recall-point based AP\n    :return: average precision\n    '
    if use_07_metric:
        ap = 0.0
        for t in np.arange(0.0, 1.1, 0.1):
            if (np.sum((rec >= t)) == 0):
                p = 0
            else:
                p = np.max(prec[(rec >= t)])
            ap += (p / 11.0)
    else:
        mrec = np.concatenate([0.0], rec, [1.0])
        mpre = np.concatenate([0.0], prec, [0.0])
        for i in range((mpre.size - 1), 0, (- 1)):
            mpre[(i - 1)] = np.maximum(mpre[(i - 1)], mpre[i])
        i = np.where((mrec[1:] != mrec[:(- 1)]))[0]
        ap = np.sum(((mrec[(i + 1)] - mrec[i]) * mpre[(i + 1)]))
    return ap
