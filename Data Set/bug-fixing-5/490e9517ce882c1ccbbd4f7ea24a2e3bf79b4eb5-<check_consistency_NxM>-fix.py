def check_consistency_NxM(sym_list, ctx_list):
    check_consistency(np.repeat(sym_list, len(ctx_list)), (ctx_list * len(sym_list)), scale=0.5)