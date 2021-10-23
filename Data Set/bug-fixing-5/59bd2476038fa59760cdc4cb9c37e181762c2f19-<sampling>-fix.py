def sampling(args):
    (z_mean, z_log_var) = args
    epsilon = K.random_normal(shape=(batch_size, latent_dim), mean=0.0)
    return (z_mean + (K.exp((z_log_var / 2)) * epsilon))