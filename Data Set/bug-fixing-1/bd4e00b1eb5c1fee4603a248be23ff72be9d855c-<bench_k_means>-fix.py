

def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print(('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f' % (name, (time() - t0), estimator.inertia_, metrics.homogeneity_score(labels, estimator.labels_), metrics.completeness_score(labels, estimator.labels_), metrics.v_measure_score(labels, estimator.labels_), metrics.adjusted_rand_score(labels, estimator.labels_), metrics.adjusted_mutual_info_score(labels, estimator.labels_), metrics.silhouette_score(data, estimator.labels_, metric='euclidean', sample_size=sample_size))))
