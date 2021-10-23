

def upsample_bilinear2d(g, input, output_size):
    w_scale = (float(output_size[(- 1)]) / input.type().sizes()[(- 1)])
    h_scale = (float(output_size[(- 2)]) / input.type().sizes()[(- 2)])
    return g.op('Upsample', input, width_scale_f=w_scale, height_scale_f=h_scale, mode_s='bilinear')
