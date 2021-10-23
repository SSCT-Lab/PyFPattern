def sample_rois(rois, fg_rois_per_image, rois_per_image, num_classes, labels=None, overlaps=None, bbox_targets=None, gt_boxes=None):
    '\n    generate random sample of ROIs comprising foreground and background examples\n    :param rois: all_rois [n, 4]; e2e: [n, 5] with batch_index\n    :param fg_rois_per_image: foreground roi number\n    :param rois_per_image: total roi number\n    :param num_classes: number of classes\n    :param labels: maybe precomputed\n    :param overlaps: maybe precomputed (max_overlaps)\n    :param bbox_targets: maybe precomputed\n    :param gt_boxes: optional for e2e [n, 5] (x1, y1, x2, y2, cls)\n    :return: (labels, rois, bbox_targets, bbox_weights)\n    '
    if (labels is None):
        overlaps = bbox_overlaps(rois[:, 1:].astype(np.float), gt_boxes[:, :4].astype(np.float))
        gt_assignment = overlaps.argmax(axis=1)
        overlaps = overlaps.max(axis=1)
        labels = gt_boxes[(gt_assignment, 4)]
    fg_indexes = np.where((overlaps >= config.TRAIN.FG_THRESH))[0]
    fg_rois_per_this_image = np.minimum(fg_rois_per_image, fg_indexes.size)
    if (len(fg_indexes) > fg_rois_per_this_image):
        fg_indexes = npr.choice(fg_indexes, size=fg_rois_per_this_image, replace=False)
    bg_indexes = np.where(((overlaps < config.TRAIN.BG_THRESH_HI) & (overlaps >= config.TRAIN.BG_THRESH_LO)))[0]
    bg_rois_per_this_image = (rois_per_image - fg_rois_per_this_image)
    bg_rois_per_this_image = np.minimum(bg_rois_per_this_image, bg_indexes.size)
    if (len(bg_indexes) > bg_rois_per_this_image):
        bg_indexes = npr.choice(bg_indexes, size=bg_rois_per_this_image, replace=False)
    keep_indexes = np.append(fg_indexes, bg_indexes)
    neg_idx = np.where((overlaps < config.TRAIN.FG_THRESH))[0]
    neg_rois = rois[neg_idx]
    while (keep_indexes.shape[0] < rois_per_image):
        gap = np.minimum(len(neg_rois), (rois_per_image - keep_indexes.shape[0]))
        gap_indexes = npr.choice(range(len(neg_rois)), size=gap, replace=False)
        keep_indexes = np.append(keep_indexes, neg_idx[gap_indexes])
    labels = labels[keep_indexes]
    labels[fg_rois_per_this_image:] = 0
    rois = rois[keep_indexes]
    if (bbox_targets is not None):
        bbox_target_data = bbox_targets[keep_indexes, :]
    else:
        targets = bbox_transform(rois[:, 1:], gt_boxes[gt_assignment[keep_indexes], :4])
        if config.TRAIN.BBOX_NORMALIZATION_PRECOMPUTED:
            targets = ((targets - np.array(config.TRAIN.BBOX_MEANS)) / np.array(config.TRAIN.BBOX_STDS))
        bbox_target_data = np.hstack((labels[:, np.newaxis], targets))
    (bbox_targets, bbox_weights) = expand_bbox_regression_targets(bbox_target_data, num_classes)
    return (rois, labels, bbox_targets, bbox_weights)