def response_closure(module, question, responses):
    resp_gen = (('%s\n' % str(r).rstrip('\n').decode()) for r in responses)

    def wrapped(info):
        try:
            return resp_gen.next()
        except StopIteration:
            module.fail_json(msg=("No remaining responses for '%s', output was '%s'" % (question, info['child_result_list'][(- 1)])))
    return wrapped