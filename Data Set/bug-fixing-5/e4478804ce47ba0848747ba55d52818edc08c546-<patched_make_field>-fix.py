def patched_make_field(self, types, domain, items, **kw):

    def handle_item(fieldarg, content):
        par = nodes.paragraph()
        par += addnodes.literal_strong('', fieldarg)
        if (fieldarg in types):
            par += nodes.Text(' (')
            fieldtype = types.pop(fieldarg)
            if ((len(fieldtype) == 1) and isinstance(fieldtype[0], nodes.Text)):
                typename = ''.join((n.astext() for n in fieldtype))
                typename = typename.replace('int', 'python:int')
                typename = typename.replace('long', 'python:long')
                typename = typename.replace('float', 'python:float')
                typename = typename.replace('type', 'python:type')
                par.extend(self.make_xrefs(self.typerolename, domain, typename, addnodes.literal_emphasis, **kw))
            else:
                par += fieldtype
            par += nodes.Text(')')
        par += nodes.Text(' -- ')
        par += content
        return par
    fieldname = nodes.field_name('', self.label)
    if ((len(items) == 1) and self.can_collapse):
        (fieldarg, content) = items[0]
        bodynode = handle_item(fieldarg, content)
    else:
        bodynode = self.list_type()
        for (fieldarg, content) in items:
            bodynode += nodes.list_item('', handle_item(fieldarg, content))
    fieldbody = nodes.field_body('', bodynode)
    return nodes.field('', fieldname, fieldbody)