def modified_huber_loss_forward(val):
    if (val < (- 1)):
        return ((- 4) * val)
    elif (val < 1):
        return ((1 - val) * (1 - val))
    else:
        return 0