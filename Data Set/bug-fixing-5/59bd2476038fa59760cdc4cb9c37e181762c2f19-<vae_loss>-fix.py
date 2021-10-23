def vae_loss(x, x_decoded_mean):
    xent_loss = (original_dim * objectives.binary_crossentropy(x, x_decoded_mean))
    kl_loss = ((- 0.5) * K.sum((((1 + z_log_var) - K.square(z_mean)) - K.exp(z_log_var)), axis=(- 1)))
    return (xent_loss + kl_loss)