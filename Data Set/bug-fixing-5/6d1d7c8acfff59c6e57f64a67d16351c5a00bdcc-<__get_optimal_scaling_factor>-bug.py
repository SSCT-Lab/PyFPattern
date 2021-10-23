def __get_optimal_scaling_factor(self, activation_blob, num_quantized_bins=255):
    '\n        Using the KL-divergenc method to get the more precise scaling factor.\n        '
    max_val = np.max(activation_blob)
    min_val = np.min(activation_blob)
    if (min_val >= 0):
        (hist, hist_edeges) = np.histogram(activation_blob, bins=2048, range=(min_val, max_val))
        ending_iter = 2047
        starting_iter = int((ending_iter * 0.7))
    else:
        th = max(abs(max_val), abs(min_val))
        (hist, hist_edeges) = np.histogram(activation_blob, bins=2048, range=((- th), th))
        starting_iter = 0
        ending_iter = 2047
        if (abs(max_val) > abs(min_val)):
            while (starting_iter < ending_iter):
                if (hist[starting_iter] == 0):
                    starting_iter += 1
                    continue
                else:
                    break
            starting_iter += int(((ending_iter - starting_iter) * 0.6))
        else:
            while (ending_iter > 0):
                if (hist[ending_iter] == 0):
                    ending_iter -= 1
                    continue
                else:
                    break
            starting_iter = int((0.6 * ending_iter))
    bin_width = (hist_edeges[1] - hist_edeges[0])
    P_sum = len(activation_blob)
    min_kl_divergence = 0
    min_kl_index = 0
    kl_inited = False
    for i in range(starting_iter, (ending_iter + 1)):
        reference_distr_P = hist[0:i].tolist()
        outliers_count = sum(hist[i:2048])
        if (reference_distr_P[(i - 1)] == 0):
            continue
        reference_distr_P[(i - 1)] += outliers_count
        reference_distr_bins = reference_distr_P[:]
        candidate_distr_Q = hist[0:i].tolist()
        num_merged_bins = (i / num_quantized_bins)
        candidate_distr_Q_quantized = ([0] * num_quantized_bins)
        j_start = 0
        j_end = num_merged_bins
        for idx in xrange(num_quantized_bins):
            candidate_distr_Q_quantized[idx] = sum(candidate_distr_Q[j_start:j_end])
            j_start += num_merged_bins
            j_end += num_merged_bins
            if ((idx + 1) == (num_quantized_bins - 1)):
                j_end = i
        candidate_distr_Q = self.__expand_quantized_bins(candidate_distr_Q_quantized, reference_distr_bins)
        Q_sum = sum(candidate_distr_Q)
        kl_divergence = self.__safe_entropy(reference_distr_P, P_sum, candidate_distr_Q, Q_sum)
        if (not kl_inited):
            min_kl_divergence = kl_divergence
            min_kl_index = i
            kl_inited = True
        elif (kl_divergence < min_kl_divergence):
            min_kl_divergence = kl_divergence
            min_kl_index = i
        else:
            pass
    if (min_kl_index == 0):
        while (starting_iter > 0):
            if (hist[starting_iter] == 0):
                starting_iter -= 1
                continue
            else:
                break
        min_kl_index = starting_iter
    return ((min_kl_index + 0.5) * bin_width)