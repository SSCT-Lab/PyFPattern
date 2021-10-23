def _create_storer(self, group, format=None, value=None, **kwargs) -> Union[('GenericFixed', 'Table')]:
    ' return a suitable class to operate '

    def error(t):
        return TypeError(f'cannot properly create the storer for: [{t}] [group->{group},value->{type(value)},format->{format},kwargs->{kwargs}]')
    pt = _ensure_decoded(getattr(group._v_attrs, 'pandas_type', None))
    tt = _ensure_decoded(getattr(group._v_attrs, 'table_type', None))
    if (pt is None):
        if (value is None):
            _tables()
            assert (_table_mod is not None)
            if (getattr(group, 'table', None) or isinstance(group, _table_mod.table.Table)):
                pt = 'frame_table'
                tt = 'generic_table'
            else:
                raise TypeError('cannot create a storer if the object is not existing nor a value are passed')
        else:
            _TYPE_MAP = {
                Series: 'series',
                DataFrame: 'frame',
            }
            try:
                pt = _TYPE_MAP[type(value)]
            except KeyError:
                raise error('_TYPE_MAP')
            if (format == 'table'):
                pt += '_table'
    if ('table' not in pt):
        try:
            return globals()[_STORER_MAP[pt]](self, group, **kwargs)
        except KeyError:
            raise error('_STORER_MAP')
    if (tt is None):
        if (value is not None):
            if (pt == 'series_table'):
                index = getattr(value, 'index', None)
                if (index is not None):
                    if (index.nlevels == 1):
                        tt = 'appendable_series'
                    elif (index.nlevels > 1):
                        tt = 'appendable_multiseries'
            elif (pt == 'frame_table'):
                index = getattr(value, 'index', None)
                if (index is not None):
                    if (index.nlevels == 1):
                        tt = 'appendable_frame'
                    elif (index.nlevels > 1):
                        tt = 'appendable_multiframe'
            elif (pt == 'wide_table'):
                tt = 'appendable_panel'
            elif (pt == 'ndim_table'):
                tt = 'appendable_ndim'
        else:
            tt = 'legacy_panel'
            try:
                fields = group.table._v_attrs.fields
                if ((len(fields) == 1) and (fields[0] == 'value')):
                    tt = 'legacy_frame'
            except IndexError:
                pass
    try:
        return globals()[_TABLE_MAP[tt]](self, group, **kwargs)
    except KeyError:
        raise error('_TABLE_MAP')