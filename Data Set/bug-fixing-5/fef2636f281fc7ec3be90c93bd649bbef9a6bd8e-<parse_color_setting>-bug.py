def parse_color_setting(config_string):
    'Parse a DJANGO_COLORS environment variable to produce the system palette\n\n    The general form of a palette definition is:\n\n        "palette;role=fg;role=fg/bg;role=fg,option,option;role=fg/bg,option,option"\n\n    where:\n        palette is a named palette; one of \'light\', \'dark\', or \'nocolor\'.\n        role is a named style used by Django\n        fg is a background color.\n        bg is a background color.\n        option is a display options.\n\n    Specifying a named palette is the same as manually specifying the individual\n    definitions for each role. Any individual definitions following the palette\n    definition will augment the base palette definition.\n\n    Valid roles:\n        \'error\', \'success\', \'warning\', \'notice\', \'sql_field\', \'sql_coltype\',\n        \'sql_keyword\', \'sql_table\', \'http_info\', \'http_success\',\n        \'http_redirect\', \'http_not_modified\', \'http_bad_request\',\n        \'http_not_found\', \'http_server_error\', \'migrate_heading\',\n        \'migrate_label\'\n\n    Valid colors:\n        \'black\', \'red\', \'green\', \'yellow\', \'blue\', \'magenta\', \'cyan\', \'white\'\n\n    Valid options:\n        \'bold\', \'underscore\', \'blink\', \'reverse\', \'conceal\', \'noreset\'\n    '
    if (not config_string):
        return PALETTES[DEFAULT_PALETTE]
    parts = config_string.lower().split(';')
    palette = PALETTES[NOCOLOR_PALETTE].copy()
    for part in parts:
        if (part in PALETTES):
            palette.update(PALETTES[part])
        elif ('=' in part):
            definition = {
                
            }
            (role, instructions) = part.split('=')
            role = role.upper()
            styles = instructions.split(',')
            styles.reverse()
            colors = styles.pop().split('/')
            colors.reverse()
            fg = colors.pop()
            if (fg in color_names):
                definition['fg'] = fg
            if (colors and (colors[(- 1)] in color_names)):
                definition['bg'] = colors[(- 1)]
            opts = tuple((s for s in styles if (s in opt_dict)))
            if opts:
                definition['opts'] = opts
            if ((role in PALETTES[NOCOLOR_PALETTE]) and definition):
                palette[role] = definition
    if (palette == PALETTES[NOCOLOR_PALETTE]):
        return None
    return palette