def batch_intersection_union(output, target, nclass):
    'mIoU'
    mini = 1
    maxi = nclass
    nbins = nclass
    predict = (np.argmax(output.asnumpy().astype('int64'), 1) + 1)
    target = (target.asnumpy().astype('int64') + 1)
    predict = (predict * (target > 0).astype(predict.dtype))
    intersection = (predict * (predict == target))
    (area_inter, _) = np.histogram(intersection, bins=nbins, range=(mini, maxi))
    (area_pred, _) = np.histogram(predict, bins=nbins, range=(mini, maxi))
    (area_lab, _) = np.histogram(target, bins=nbins, range=(mini, maxi))
    area_union = ((area_pred + area_lab) - area_inter)
    assert (area_inter <= area_union).all(), 'Intersection area should be smaller than Union area'
    return (area_inter, area_union)