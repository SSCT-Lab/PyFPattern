def _sort_labels(uniques, left, right):
    if (not isinstance(uniques, np.ndarray)):
        uniques = Index(uniques).values
    llength = len(left)
    labels = np.concatenate([left, right])
    (_, new_labels) = sorting.safe_sort(uniques, labels, na_sentinel=(- 1))
    new_labels = _ensure_int64(new_labels)
    (new_left, new_right) = (new_labels[:llength], new_labels[llength:])
    return (new_left, new_right)