def vae_loss(x, x_decoded_mean):
    xent_loss = objectives.binary_crossentropy(x, x_decoded_mean)
    kl_loss = ((- 0.5) * K.mean((((1 + z_log_std) - K.square(z_mean)) - K.exp(z_log_std)), axis=(- 1)))
    return (xent_loss + kl_loss)