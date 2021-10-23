

def fill_buf(buf, i, img, shape):
    n = (buf.shape[0] // shape[1])
    m = (buf.shape[1] // shape[0])
    sx = ((i % m) * shape[0])
    sy = ((i // m) * shape[1])
    buf[sy:(sy + shape[1]), sx:(sx + shape[0]), :] = img
    return None
