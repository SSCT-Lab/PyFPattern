

def selu(x):
    'Scaled Exponential Linear Unit (SELU).\n\n    SELU is equal to: `scale * elu(x, alpha)`, where alpha and scale\n    are pre-defined constants. The values of `alpha` and `scale` are\n    chosen so that the mean and variance of the inputs are preserved\n    between two consecutive layers as long as the weights are initialized\n    correctly (see `lecun_normal` initialization) and the number of inputs\n    is "large enough" (see references for more information).\n\n    # Arguments\n        x: A tensor or variable to compute the activation function for.\n\n    # Returns\n       The scaled exponential unit activation: `scale * elu(x, alpha)`.\n\n    # Note\n        - To be used together with the initialization "lecun_normal".\n        - To be used together with the dropout variant "AlphaDropout".\n\n    # References\n        - [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)\n    '
    alpha = 1.6732632423543772
    scale = 1.0507009873554805
    return (scale * K.elu(x, alpha))
