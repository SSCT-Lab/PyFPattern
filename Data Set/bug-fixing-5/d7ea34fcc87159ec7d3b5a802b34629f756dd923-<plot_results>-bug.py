def plot_results(models, data, batch_size=128, model_name='vae_mnist'):
    'Plots labels and MNIST digits as a function of the 2D latent vector\n\n    # Arguments\n        models (tuple): encoder and decoder models\n        data (tuple): test data and label\n        batch_size (int): prediction batch size\n        model_name (string): which model is using this function\n    '
    (encoder, decoder) = models
    (x_test, y_test) = data
    os.makedirs(model_name, exist_ok=True)
    filename = os.path.join(model_name, 'vae_mean.png')
    (z_mean, _, _) = encoder.predict(x_test, batch_size=batch_size)
    plt.figure(figsize=(12, 10))
    plt.scatter(z_mean[:, 0], z_mean[:, 1], c=y_test)
    plt.colorbar()
    plt.xlabel('z[0]')
    plt.ylabel('z[1]')
    plt.savefig(filename)
    plt.show()
    filename = os.path.join(model_name, 'digits_over_latent.png')
    n = 30
    digit_size = 28
    figure = np.zeros(((digit_size * n), (digit_size * n)))
    grid_x = np.linspace((- 4), 4, n)
    grid_y = np.linspace((- 4), 4, n)[::(- 1)]
    for (i, yi) in enumerate(grid_y):
        for (j, xi) in enumerate(grid_x):
            z_sample = np.array([[xi, yi]])
            x_decoded = decoder.predict(z_sample)
            digit = x_decoded[0].reshape(digit_size, digit_size)
            figure[(i * digit_size):((i + 1) * digit_size), (j * digit_size):((j + 1) * digit_size)] = digit
    plt.figure(figsize=(10, 10))
    start_range = (digit_size // 2)
    end_range = (((n * digit_size) + start_range) + 1)
    pixel_range = np.arange(start_range, end_range, digit_size)
    sample_range_x = np.round(grid_x, 1)
    sample_range_y = np.round(grid_y, 1)
    plt.xticks(pixel_range, sample_range_x)
    plt.yticks(pixel_range, sample_range_y)
    plt.xlabel('z[0]')
    plt.ylabel('z[1]')
    plt.imshow(figure, cmap='Greys_r')
    plt.savefig(filename)
    plt.show()