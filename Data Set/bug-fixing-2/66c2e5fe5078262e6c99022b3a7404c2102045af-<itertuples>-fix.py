

def itertuples(self, index=True, name='Pandas'):
    '\n        Iterate over DataFrame rows as namedtuples.\n\n        Parameters\n        ----------\n        index : bool, default True\n            If True, return the index as the first element of the tuple.\n        name : str, default "Pandas"\n            The name of the returned namedtuples or None to return regular\n            tuples.\n\n        Yields\n        -------\n        collections.namedtuple\n            Yields a namedtuple for each row in the DataFrame with the first\n            field possibly being the index and following fields being the\n            column values.\n\n        Notes\n        -----\n        The column names will be renamed to positional names if they are\n        invalid Python identifiers, repeated, or start with an underscore.\n        With a large number of columns (>255), regular tuples are returned.\n\n        See Also\n        --------\n        DataFrame.iterrows : Iterate over DataFrame rows as (index, Series)\n            pairs.\n        DataFrame.iteritems : Iterate over (column name, Series) pairs.\n\n        Examples\n        --------\n        >>> df = pd.DataFrame({\'num_legs\': [4, 2], \'num_wings\': [0, 2]},\n        ...                   index=[\'dog\', \'hawk\'])\n        >>> df\n              num_legs  num_wings\n        dog          4          0\n        hawk         2          2\n        >>> for row in df.itertuples():\n        ...     print(row)\n        ...\n        Pandas(Index=\'dog\', num_legs=4, num_wings=0)\n        Pandas(Index=\'hawk\', num_legs=2, num_wings=2)\n\n        By setting the `index` parameter to False we can remove the index\n        as the first element of the tuple:\n\n        >>> for row in df.itertuples(index=False):\n        ...     print(row)\n        ...\n        Pandas(num_legs=4, num_wings=0)\n        Pandas(num_legs=2, num_wings=2)\n\n        With the `name` parameter set we set a custom name for the yielded\n        namedtuples:\n\n        >>> for row in df.itertuples(name=\'Animal\'):\n        ...     print(row)\n        ...\n        Animal(Index=\'dog\', num_legs=4, num_wings=0)\n        Animal(Index=\'hawk\', num_legs=2, num_wings=2)\n        '
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
