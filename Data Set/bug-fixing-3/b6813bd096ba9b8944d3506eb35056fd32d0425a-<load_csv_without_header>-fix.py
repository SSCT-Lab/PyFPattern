def load_csv_without_header(filename, target_dtype, features_dtype, target_column=(- 1)):
    'Load dataset from CSV file without a header row.'
    with gfile.Open(filename) as csv_file:
        data_file = csv.reader(csv_file)
        (data, target) = ([], [])
        for row in data_file:
            target.append(row.pop(target_column))
            data.append(np.asarray(row, dtype=features_dtype))
    target = np.array(target, dtype=target_dtype)
    data = np.array(data)
    return Dataset(data=data, target=target)