def sampling(args):
    (z_mean, z_log_std) = args
    epsilon = K.random_normal(shape=(batch_size, latent_dim), mean=0.0, std=epsilon_std)
    return (z_mean + (K.exp(z_log_std) * epsilon))