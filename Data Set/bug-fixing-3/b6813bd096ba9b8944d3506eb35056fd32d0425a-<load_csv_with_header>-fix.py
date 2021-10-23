def load_csv_with_header(filename, target_dtype, features_dtype, target_column=(- 1)):
    'Load dataset from CSV file with a header row.'
    with gfile.Open(filename) as csv_file:
        data_file = csv.reader(csv_file)
        header = next(data_file)
        n_samples = int(header[0])
        n_features = int(header[1])
        data = np.zeros((n_samples, n_features), dtype=features_dtype)
        target = np.zeros((n_samples,), dtype=target_dtype)
        for (i, row) in enumerate(data_file):
            target[i] = np.asarray(row.pop(target_column), dtype=target_dtype)
            data[i] = np.asarray(row, dtype=features_dtype)
    return Dataset(data=data, target=target)