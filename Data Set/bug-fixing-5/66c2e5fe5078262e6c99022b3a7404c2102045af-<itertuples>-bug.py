def itertuples(self, index=True, name='Pandas'):
    '\n        Iterate over DataFrame rows as namedtuples, with index value as first\n        element of the tuple.\n\n        Parameters\n        ----------\n        index : boolean, default True\n            If True, return the index as the first element of the tuple.\n        name : string, default "Pandas"\n            The name of the returned namedtuples or None to return regular\n            tuples.\n\n        Notes\n        -----\n        The column names will be renamed to positional names if they are\n        invalid Python identifiers, repeated, or start with an underscore.\n        With a large number of columns (>255), regular tuples are returned.\n\n        See also\n        --------\n        iterrows : Iterate over DataFrame rows as (index, Series) pairs.\n        iteritems : Iterate over (column name, Series) pairs.\n\n        Examples\n        --------\n\n        >>> df = pd.DataFrame({\'col1\': [1, 2], \'col2\': [0.1, 0.2]},\n                              index=[\'a\', \'b\'])\n        >>> df\n           col1  col2\n        a     1   0.1\n        b     2   0.2\n        >>> for row in df.itertuples():\n        ...     print(row)\n        ...\n        Pandas(Index=\'a\', col1=1, col2=0.10000000000000001)\n        Pandas(Index=\'b\', col1=2, col2=0.20000000000000001)\n\n        '
    arrays = []
    fields = []
    if index:
        arrays.append(self.index)
        fields.append('Index')
    arrays.extend((self.iloc[:, k] for k in range(len(self.columns))))
    if ((name is not None) and ((len(self.columns) + index) < 256)):
        try:
            itertuple = collections.namedtuple(name, (fields + list(self.columns)), rename=True)
            return map(itertuple._make, zip(*arrays))
        except Exception:
            pass
    return zip(*arrays)