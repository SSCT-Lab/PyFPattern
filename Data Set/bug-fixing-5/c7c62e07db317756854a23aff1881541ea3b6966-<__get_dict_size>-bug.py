def __get_dict_size(src_dict_size, trg_dict_size, src_lang):
    src_dict_size = min(src_dict_size, (TOTAL_EN_WORDS if (src_lang == 'en') else TOTAL_DE_WORDS))
    trg_dict_size = min(trg_dict_size, (TOTAL_DE_WORDS if (src_lang == 'en') else TOTAL_ENG_WORDS))
    return (src_dict_size, trg_dict_size)