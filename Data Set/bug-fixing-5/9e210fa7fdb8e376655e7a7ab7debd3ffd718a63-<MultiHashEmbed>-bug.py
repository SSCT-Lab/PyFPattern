@register_architecture('spacy.MultiHashEmbed.v1')
def MultiHashEmbed(config):
    cols = config['columns']
    width = config['width']
    rows = config['rows']
    tables = [HashEmbed(width, rows, column=cols.index('NORM'), name='embed_norm')]
    if config['use_subwords']:
        for feature in ['PREFIX', 'SUFFIX', 'SHAPE']:
            tables.append(HashEmbed(width, (rows // 2), column=cols.index(feature), name=('embed_%s' % feature.lower())))
    if config.get('@pretrained_vectors'):
        tables.append(make_layer(config['@pretrained_vectors']))
    mix = make_layer(config['@mix'])
    mix._layers[0].nI = sum((table.nO for table in tables))
    layer = uniqued(chain(concatenate(*tables), mix), column=cols.index('ORTH'))
    layer.cfg = config
    return layer