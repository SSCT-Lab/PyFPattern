

def train_and_eval():
    'Train and evaluate the model.'
    (train_file_name, test_file_name) = maybe_download()
    df_train = pd.read_csv(tf.gfile.Open(train_file_name), names=COLUMNS, skipinitialspace=True, engine='python')
    df_test = pd.read_csv(tf.gfile.Open(test_file_name), names=COLUMNS, skipinitialspace=True, skiprows=1, engine='python')
    df_train[LABEL_COLUMN] = df_train['income_bracket'].apply((lambda x: ('>50K' in x))).astype(int)
    df_test[LABEL_COLUMN] = df_test['income_bracket'].apply((lambda x: ('>50K' in x))).astype(int)
    model_dir = (tempfile.mkdtemp() if (not FLAGS.model_dir) else FLAGS.model_dir)
    print(('model directory = %s' % model_dir))
    m = build_estimator(model_dir)
    m.fit(input_fn=(lambda : input_fn(df_train)), steps=FLAGS.train_steps)
    results = m.evaluate(input_fn=(lambda : input_fn(df_test)), steps=1)
    for key in sorted(results):
        print(('%s: %s' % (key, results[key])))
