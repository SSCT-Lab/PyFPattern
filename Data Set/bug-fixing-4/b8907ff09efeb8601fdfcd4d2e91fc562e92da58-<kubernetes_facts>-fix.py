def kubernetes_facts(self, kind, api_version, name=None, namespace=None, label_selectors=None, field_selectors=None):
    resource = self.find_resource(kind, api_version)
    try:
        result = resource.get(name=name, namespace=namespace, label_selector=','.join(label_selectors), field_selector=','.join(field_selectors)).to_dict()
    except openshift.dynamic.exceptions.NotFoundError:
        return dict(items=[])
    if ('items' in result):
        return result
    else:
        return dict(items=[result])