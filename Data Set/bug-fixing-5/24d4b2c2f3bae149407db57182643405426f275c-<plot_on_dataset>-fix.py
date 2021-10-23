def plot_on_dataset(X, y, ax, name):
    print(('\nlearning on dataset %s' % name))
    ax.set_title(name)
    X = MinMaxScaler().fit_transform(X)
    mlps = []
    if (name == 'digits'):
        max_iter = 15
    else:
        max_iter = 400
    for (label, param) in zip(labels, params):
        print(('training: %s' % label))
        mlp = MLPClassifier(verbose=0, random_state=0, max_iter=max_iter, **param)
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=ConvergenceWarning, module='sklearn')
            mlp.fit(X, y)
        mlps.append(mlp)
        print(('Training set score: %f' % mlp.score(X, y)))
        print(('Training set loss: %f' % mlp.loss_))
    for (mlp, label, args) in zip(mlps, labels, plot_args):
        ax.plot(mlp.loss_curve_, label=label, **args)