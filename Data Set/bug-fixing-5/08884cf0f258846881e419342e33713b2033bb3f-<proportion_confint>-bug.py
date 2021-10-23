def proportion_confint(count, nobs, alpha=0.05, method='normal'):
    'confidence interval for a binomial proportion\n\n    Parameters\n    ----------\n    count : int or array\n        number of successes\n    nobs : int\n        total number of trials\n    alpha : float in (0, 1)\n        significance level, default 0.05\n    method : string in [\'normal\']\n        method to use for confidence interval,\n        currently available methods :\n\n         - `normal` : asymptotic normal approximation\n         - `agresti_coull` : Agresti-Coull interval\n         - `beta` : Clopper-Pearson interval based on Beta distribution\n         - `wilson` : Wilson Score interval\n         - `jeffrey` : Jeffrey\'s Bayesian Interval\n         - `binom_test` : experimental, inversion of binom_test\n\n    Returns\n    -------\n    ci_low, ci_upp : float\n        lower and upper confidence level with coverage (approximately) 1-alpha.\n        Note: Beta has coverage\n        coverage is only 1-alpha on average for some other methods.)\n\n    Notes\n    -----\n    Beta, the Clopper-Pearson interval has coverage at least 1-alpha, but is\n    in general conservative. Most of the other methods have average coverage\n    equal to 1-alpha, but will have smaller coverage in some cases.\n\n    Method "binom_test" directly inverts the binomial test in scipy.stats.\n    which has discrete steps.\n\n    TODO: binom_test intervals raise an exception in small samples if one\n       interval bound is close to zero or one.\n\n    References\n    ----------\n    http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval\n\n    Brown, Lawrence D.; Cai, T. Tony; DasGupta, Anirban (2001). "Interval\n        Estimation for a Binomial Proportion",\n        Statistical Science 16 (2): 101–133. doi:10.1214/ss/1009213286.\n        TODO: Is this the correct one ?\n\n    '
    q_ = ((count * 1.0) / nobs)
    alpha_2 = (0.5 * alpha)
    if (method == 'normal'):
        std_ = np.sqrt(((q_ * (1 - q_)) / nobs))
        dist = (stats.norm.isf((alpha / 2.0)) * std_)
        ci_low = (q_ - dist)
        ci_upp = (q_ + dist)
    elif (method == 'binom_test'):

        def func(qi):
            return (stats.binom_test((q_ * nobs), nobs, p=qi) - alpha)
        ci_low = optimize.brentq(func, (q_ * 0.1), q_)
        ub = np.minimum((q_ + (2 * (q_ - ci_low))), 1)
        ci_upp = optimize.brentq(func, q_, ub)
    elif (method == 'beta'):
        ci_low = stats.beta.ppf(alpha_2, count, ((nobs - count) + 1))
        ci_upp = stats.beta.isf(alpha_2, (count + 1), (nobs - count))
    elif (method == 'agresti_coull'):
        crit = stats.norm.isf((alpha / 2.0))
        nobs_c = (nobs + (crit ** 2))
        q_c = ((count + ((crit ** 2) / 2.0)) / nobs_c)
        std_c = np.sqrt(((q_c * (1.0 - q_c)) / nobs_c))
        dist = (crit * std_c)
        ci_low = (q_c - dist)
        ci_upp = (q_c + dist)
    elif (method == 'wilson'):
        crit = stats.norm.isf((alpha / 2.0))
        crit2 = (crit ** 2)
        denom = (1 + (crit2 / nobs))
        center = ((q_ + (crit2 / (2 * nobs))) / denom)
        dist = (crit * np.sqrt((((q_ * (1.0 - q_)) / nobs) + (crit2 / (4.0 * (nobs ** 2))))))
        dist /= denom
        ci_low = (center - dist)
        ci_upp = (center + dist)
    elif (method == 'jeffrey'):
        (ci_low, ci_upp) = stats.beta.interval((1 - alpha), (count + 0.5), ((nobs - count) + 0.5))
    else:
        raise NotImplementedError(('method "%s" is not available' % method))
    return (ci_low, ci_upp)