

@action('varexport', 'Export', '', single=False)
def action_varexport(self, items):
    var_dict = {
        
    }
    d = json.JSONDecoder()
    for var in items:
        try:
            val = d.decode(var.val)
        except Exception:
            val = var.val
        var_dict[var.key] = val
    response = make_response(json.dumps(var_dict, sort_keys=True, indent=4))
    response.headers['Content-Disposition'] = 'attachment; filename=variables.json'
    return response
