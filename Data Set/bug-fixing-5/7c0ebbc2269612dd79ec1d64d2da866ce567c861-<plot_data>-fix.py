def plot_data(lda, X, y, y_pred, fig_index):
    splot = plt.subplot(2, 2, fig_index)
    if (fig_index == 1):
        plt.title('Linear Discriminant Analysis')
        plt.ylabel('Data with fixed covariance')
    elif (fig_index == 2):
        plt.title('Quadratic Discriminant Analysis')
    elif (fig_index == 3):
        plt.ylabel('Data with varying covariances')
    tp = (y == y_pred)
    (tp0, tp1) = (tp[(y == 0)], tp[(y == 1)])
    (X0, X1) = (X[(y == 0)], X[(y == 1)])
    (X0_tp, X0_fp) = (X0[tp0], X0[(~ tp0)])
    (X1_tp, X1_fp) = (X1[tp1], X1[(~ tp1)])
    alpha = 0.5
    plt.plot(X0_tp[:, 0], X0_tp[:, 1], 'o', alpha=alpha, color='red')
    plt.plot(X0_fp[:, 0], X0_fp[:, 1], '*', alpha=alpha, color='#990000')
    plt.plot(X1_tp[:, 0], X1_tp[:, 1], 'o', alpha=alpha, color='blue')
    plt.plot(X1_fp[:, 0], X1_fp[:, 1], '*', alpha=alpha, color='#000099')
    (nx, ny) = (200, 100)
    (x_min, x_max) = plt.xlim()
    (y_min, y_max) = plt.ylim()
    (xx, yy) = np.meshgrid(np.linspace(x_min, x_max, nx), np.linspace(y_min, y_max, ny))
    Z = lda.predict_proba(np.c_[(xx.ravel(), yy.ravel())])
    Z = Z[:, 1].reshape(xx.shape)
    plt.pcolormesh(xx, yy, Z, cmap='red_blue_classes', norm=colors.Normalize(0.0, 1.0))
    plt.contour(xx, yy, Z, [0.5], linewidths=2.0, colors='k')
    plt.plot(lda.means_[0][0], lda.means_[0][1], 'o', color='black', markersize=10)
    plt.plot(lda.means_[1][0], lda.means_[1][1], 'o', color='black', markersize=10)
    return splot