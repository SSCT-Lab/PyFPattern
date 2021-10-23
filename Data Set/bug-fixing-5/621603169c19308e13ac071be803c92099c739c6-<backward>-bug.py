@staticmethod
def backward(ctx, grad_output):
    (result,) = ctx.saved_variables
    return Variable(result.data.new(1).expand_as(result))