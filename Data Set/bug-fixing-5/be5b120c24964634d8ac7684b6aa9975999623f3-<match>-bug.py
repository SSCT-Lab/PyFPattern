def match(refs, img):
    best_score = 10
    best_name = None
    lbp = local_binary_pattern(img, n_points, radius, METHOD)
    n_bins = int((lbp.max() + 1))
    (hist, _) = np.histogram(lbp, normed=True, bins=n_bins, range=(0, n_bins))
    for (name, ref) in refs.items():
        (ref_hist, _) = np.histogram(ref, normed=True, bins=n_bins, range=(0, n_bins))
        score = kullback_leibler_divergence(hist, ref_hist)
        if (score < best_score):
            best_score = score
            best_name = name
    return best_name