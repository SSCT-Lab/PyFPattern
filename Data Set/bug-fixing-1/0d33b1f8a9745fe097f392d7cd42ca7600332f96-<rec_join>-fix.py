

def rec_join(key, r1, r2, jointype='inner', defaults=None, r1postfix='1', r2postfix='2'):
    "\n    Join record arrays *r1* and *r2* on *key*; *key* is a tuple of\n    field names -- if *key* is a string it is assumed to be a single\n    attribute name. If *r1* and *r2* have equal values on all the keys\n    in the *key* tuple, then their fields will be merged into a new\n    record array containing the intersection of the fields of *r1* and\n    *r2*.\n\n    *r1* (also *r2*) must not have any duplicate keys.\n\n    The *jointype* keyword can be 'inner', 'outer', 'leftouter'.  To\n    do a rightouter join just reverse *r1* and *r2*.\n\n    The *defaults* keyword is a dictionary filled with\n    ``{column_name:default_value}`` pairs.\n\n    The keywords *r1postfix* and *r2postfix* are postfixed to column names\n    (other than keys) that are both in *r1* and *r2*.\n    "
    if cbook.is_string_like(key):
        key = (key,)
    for name in key:
        if (name not in r1.dtype.names):
            raise ValueError(('r1 does not have key field %s' % name))
        if (name not in r2.dtype.names):
            raise ValueError(('r2 does not have key field %s' % name))

    def makekey(row):
        return tuple([row[name] for name in key])
    r1d = dict([(makekey(row), i) for (i, row) in enumerate(r1)])
    r2d = dict([(makekey(row), i) for (i, row) in enumerate(r2)])
    r1keys = set(r1d.keys())
    r2keys = set(r2d.keys())
    common_keys = (r1keys & r2keys)
    r1ind = np.array([r1d[k] for k in common_keys])
    r2ind = np.array([r2d[k] for k in common_keys])
    common_len = len(common_keys)
    left_len = right_len = 0
    if ((jointype == 'outer') or (jointype == 'leftouter')):
        left_keys = r1keys.difference(r2keys)
        left_ind = np.array([r1d[k] for k in left_keys])
        left_len = len(left_ind)
    if (jointype == 'outer'):
        right_keys = r2keys.difference(r1keys)
        right_ind = np.array([r2d[k] for k in right_keys])
        right_len = len(right_ind)

    def key_desc(name):
        '\n        if name is a string key, use the larger size of r1 or r2 before\n        merging\n        '
        dt1 = r1.dtype[name]
        if (dt1.type != np.string_):
            return (name, dt1.descr[0][1])
        dt2 = r2.dtype[name]
        if (dt1 != dt2):
            msg = "The '{0}' fields in arrays 'r1' and 'r2' must have the same"
            msg += ' dtype.'
            raise ValueError(msg.format(name))
        if (dt1.num > dt2.num):
            return (name, dt1.descr[0][1])
        else:
            return (name, dt2.descr[0][1])
    keydesc = [key_desc(name) for name in key]

    def mapped_r1field(name):
        '\n        The column name in *newrec* that corresponds to the column in *r1*.\n        '
        if ((name in key) or (name not in r2.dtype.names)):
            return name
        else:
            return (name + r1postfix)

    def mapped_r2field(name):
        '\n        The column name in *newrec* that corresponds to the column in *r2*.\n        '
        if ((name in key) or (name not in r1.dtype.names)):
            return name
        else:
            return (name + r2postfix)
    r1desc = [(mapped_r1field(desc[0]), desc[1]) for desc in r1.dtype.descr if (desc[0] not in key)]
    r2desc = [(mapped_r2field(desc[0]), desc[1]) for desc in r2.dtype.descr if (desc[0] not in key)]
    newdtype = np.dtype(((keydesc + r1desc) + r2desc))
    newrec = np.recarray((((common_len + left_len) + right_len),), dtype=newdtype)
    if (defaults is not None):
        for thiskey in defaults:
            if (thiskey not in newdtype.names):
                warnings.warn(('rec_join defaults key="%s" not in new dtype names "%s"' % (thiskey, newdtype.names)))
    for name in newdtype.names:
        dt = newdtype[name]
        if (dt.kind in ('f', 'i')):
            newrec[name] = 0
    if ((jointype != 'inner') and (defaults is not None)):
        newrec_fields = list(six.iterkeys(newrec.dtype.fields))
        for (k, v) in six.iteritems(defaults):
            if (k in newrec_fields):
                newrec[k] = v
    for field in r1.dtype.names:
        newfield = mapped_r1field(field)
        if common_len:
            newrec[newfield][:common_len] = r1[field][r1ind]
        if (((jointype == 'outer') or (jointype == 'leftouter')) and left_len):
            newrec[newfield][common_len:(common_len + left_len)] = r1[field][left_ind]
    for field in r2.dtype.names:
        newfield = mapped_r2field(field)
        if ((field not in key) and common_len):
            newrec[newfield][:common_len] = r2[field][r2ind]
        if ((jointype == 'outer') and right_len):
            newrec[newfield][(- right_len):] = r2[field][right_ind]
    newrec.sort(order=key)
    return newrec
