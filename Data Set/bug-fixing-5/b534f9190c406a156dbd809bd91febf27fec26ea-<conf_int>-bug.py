def conf_int(self, obs=False, alpha=0.05):
    '\n        Returns the confidence interval of the value, `effect` of the constraint.\n\n        This is currently only available for t and z tests.\n\n        Parameters\n        ----------\n        alpha : float, optional\n            The significance level for the confidence interval.\n            ie., The default `alpha` = .05 returns a 95% confidence interval.\n\n        Returns\n        -------\n        ci : ndarray, (k_constraints, 2)\n            The array has the lower and the upper limit of the confidence\n            interval in the columns.\n\n        '
    se = (self.se_obs if obs else self.se_mean)
    q = self.dist.ppf((1 - (alpha / 2.0)), *self.dist_args)
    lower = (self.predicted_mean - (q * se))
    upper = (self.predicted_mean + (q * se))
    return np.column_stack((lower, upper))