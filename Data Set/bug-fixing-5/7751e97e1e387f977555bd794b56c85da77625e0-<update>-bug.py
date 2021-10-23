def update(module, link):
    delete(module, self_link(module))
    create(module, self_link(module))