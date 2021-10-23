def least_squares_discriminator_loss(discriminator_real_outputs, discriminator_gen_outputs, real_label=1, fake_label=0, real_weights=1.0, generated_weights=1.0, scope=None, loss_collection=ops.GraphKeys.LOSSES, reduction=losses.Reduction.SUM_BY_NONZERO_WEIGHTS, add_summaries=False):
    'Least squares discriminator loss.\n\n  This loss comes from `Least Squares Generative Adversarial Networks`\n  (https://arxiv.org/abs/1611.04076).\n\n  L = 1/2 * (D(x) - `real`) ** 2 +\n      1/2 * (D(G(z)) - `fake_label`) ** 2\n\n  where D(y) are discriminator logits.\n\n  Args:\n    discriminator_real_outputs: Discriminator output on real data.\n    discriminator_gen_outputs: Discriminator output on generated data. Expected\n      to be in the range of (-inf, inf).\n    real_label: The value that the discriminator tries to output for real data.\n    fake_label: The value that the discriminator tries to output for fake data.\n    real_weights: Optional `Tensor` whose rank is either 0, or the same rank as\n      `discriminator_real_outputs`, and must be broadcastable to\n      `discriminator_real_outputs` (i.e., all dimensions must be either `1`, or\n      the same as the corresponding dimension).\n    generated_weights: Same as `real_weights`, but for\n      `discriminator_gen_outputs`.\n    scope: The scope for the operations performed in computing the loss.\n    loss_collection: collection to which this loss will be added.\n    reduction: A `tf.losses.Reduction` to apply to loss.\n    add_summaries: Whether or not to add summaries for the loss.\n\n  Returns:\n    A loss Tensor. The shape depends on `reduction`.\n  '
    with ops.name_scope(scope, 'lsq_discriminator_loss', (discriminator_gen_outputs, real_label)) as scope:
        discriminator_real_outputs = math_ops.to_float(discriminator_real_outputs)
        discriminator_gen_outputs = math_ops.to_float(discriminator_gen_outputs)
        discriminator_real_outputs.shape.assert_is_compatible_with(discriminator_gen_outputs.shape)
        real_losses = (math_ops.squared_difference(discriminator_real_outputs, real_label) / 2.0)
        fake_losses = (math_ops.squared_difference(discriminator_gen_outputs, fake_label) / 2.0)
        loss_on_real = losses.compute_weighted_loss(real_losses, real_weights, scope, loss_collection=None, reduction=reduction)
        loss_on_generated = losses.compute_weighted_loss(fake_losses, generated_weights, scope, loss_collection=None, reduction=reduction)
        loss = (loss_on_real + loss_on_generated)
        util.add_loss(loss, loss_collection)
    if add_summaries:
        summary.scalar('discriminator_gen_lsq_loss', loss_on_generated)
        summary.scalar('discriminator_real_lsq_loss', loss_on_real)
        summary.scalar('discriminator_lsq_loss', loss)
    return loss