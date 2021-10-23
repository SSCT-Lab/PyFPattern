def check_filterable(self, expression):
    'Raise an error if expression cannot be used in a WHERE clause.'
    if (not getattr(expression, 'filterable', True)):
        raise NotSupportedError((expression.__class__.__name__ + ' is disallowed in the filter clause.'))
    if hasattr(expression, 'get_source_expressions'):
        for expr in expression.get_source_expressions():
            self.check_filterable(expr)