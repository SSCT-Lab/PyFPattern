def set_table_attributes(self, attributes):
    '\n        Set the table attributes.\n\n        These are the items that show up in the opening ``<table>`` tag\n        in addition to to automatic (by default) id.\n\n        Parameters\n        ----------\n        attributes : string\n\n        Returns\n        -------\n        self : Styler\n\n        Examples\n        --------\n        >>> df = pd.DataFrame(np.random.randn(10, 4))\n        >>> df.style.set_table_attributes(\'class="pure-table"\')\n        # ... <table class="pure-table"> ...\n        '
    self.table_attributes = attributes
    return self