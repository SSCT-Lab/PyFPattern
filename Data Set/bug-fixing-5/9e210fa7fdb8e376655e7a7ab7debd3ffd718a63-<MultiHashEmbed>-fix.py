@register_architecture('spacy.MultiHashEmbed.v1')
def MultiHashEmbed(config):
    cols = config['columns']
    width = config['width']
    rows = config['rows']
    norm = HashEmbed(width, rows, column=cols.index('NORM'), name='embed_norm')
    if config['use_subwords']:
        prefix = HashEmbed(width, (rows // 2), column=cols.index('PREFIX'), name='embed_prefix')
        suffix = HashEmbed(width, (rows // 2), column=cols.index('SUFFIX'), name='embed_suffix')
        shape = HashEmbed(width, (rows // 2), column=cols.index('SHAPE'), name='embed_shape')
    if config.get('@pretrained_vectors'):
        glove = make_layer(config['@pretrained_vectors'])
    mix = make_layer(config['@mix'])
    with Model.define_operators({
        '>>': chain,
        '|': concatenate,
    }):
        if (config['use_subwords'] and config['@pretrained_vectors']):
            mix._layers[0].nI = (width * 5)
            layer = uniqued((((((glove | norm) | prefix) | suffix) | shape) >> mix), column=cols.index('ORTH'))
        elif config['use_subwords']:
            mix._layers[0].nI = (width * 4)
            layer = uniqued(((((norm | prefix) | suffix) | shape) >> mix), column=cols.index('ORTH'))
        elif config['@pretrained_vectors']:
            mix._layers[0].nI = (width * 2)
            embed = uniqued(((glove | norm) >> mix), column=cols.index('ORTH'))
        else:
            embed = norm
    layer.cfg = config
    return layer