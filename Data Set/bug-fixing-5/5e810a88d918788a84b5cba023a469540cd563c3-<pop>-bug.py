def pop(self, item):
    "\n        Return item and drop from frame. Raise KeyError if not found.\n\n        Parameters\n        ----------\n        item : str\n            Label of column to be popped.\n\n        Returns\n        -------\n        Series\n\n        Examples\n        --------\n        >>> df = pd.DataFrame([('falcon', 'bird', 389.0),\n        ...                    ('parrot', 'bird', 24.0),\n        ...                    ('lion', 'mammal', 80.5),\n        ...                    ('monkey','mammal', np.nan)],\n        ...                   columns=('name', 'class', 'max_speed'))\n        >>> df\n             name   class  max_speed\n        0  falcon    bird      389.0\n        1  parrot    bird       24.0\n        2    lion  mammal       80.5\n        3  monkey  mammal        NaN\n\n        >>> df.pop('class')\n        0      bird\n        1      bird\n        2    mammal\n        3    mammal\n        Name: class, dtype: object\n\n        >>> df\n             name  max_speed\n        0  falcon      389.0\n        1  parrot       24.0\n        2    lion       80.5\n        3  monkey        NaN\n        "
    result = self[item]
    del self[item]
    try:
        result._reset_cacher()
    except AttributeError:
        pass
    return result