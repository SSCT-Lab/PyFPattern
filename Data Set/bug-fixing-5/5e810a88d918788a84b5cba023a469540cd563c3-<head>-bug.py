def head(self: FrameOrSeries, n: int=5) -> FrameOrSeries:
    "\n        Return the first `n` rows.\n\n        This function returns the first `n` rows for the object based\n        on position. It is useful for quickly testing if your object\n        has the right type of data in it.\n\n        Parameters\n        ----------\n        n : int, default 5\n            Number of rows to select.\n\n        Returns\n        -------\n        obj_head : same type as caller\n            The first `n` rows of the caller object.\n\n        See Also\n        --------\n        DataFrame.tail: Returns the last `n` rows.\n\n        Examples\n        --------\n        >>> df = pd.DataFrame({'animal':['alligator', 'bee', 'falcon', 'lion',\n        ...                    'monkey', 'parrot', 'shark', 'whale', 'zebra']})\n        >>> df\n              animal\n        0  alligator\n        1        bee\n        2     falcon\n        3       lion\n        4     monkey\n        5     parrot\n        6      shark\n        7      whale\n        8      zebra\n\n        Viewing the first 5 lines\n\n        >>> df.head()\n              animal\n        0  alligator\n        1        bee\n        2     falcon\n        3       lion\n        4     monkey\n\n        Viewing the first `n` lines (three in this case)\n\n        >>> df.head(3)\n              animal\n        0  alligator\n        1        bee\n        2     falcon\n        "
    return self.iloc[:n]