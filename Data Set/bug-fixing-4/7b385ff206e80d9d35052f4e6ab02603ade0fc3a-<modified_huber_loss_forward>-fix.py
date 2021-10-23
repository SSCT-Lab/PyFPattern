def modified_huber_loss_forward(val):
    if (val < (- 1)):
        return ((- 4.0) * val)
    elif (val < 1):
        return ((1.0 - val) * (1.0 - val))
    else:
        return 0.0