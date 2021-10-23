def _AddTool(parent, wx_ids, text, bmp, tooltip_text):
    if (text in ['Pan', 'Zoom']):
        kind = wx.ITEM_CHECK
    else:
        kind = wx.ITEM_NORMAL
    if is_phoenix:
        add_tool = parent.AddTool
    else:
        add_tool = parent.DoAddTool
    if ((not is_phoenix) or (wx_version >= str('4.0.0b2'))):
        kwargs = dict(label=text, bitmap=bmp, bmpDisabled=wx.NullBitmap, shortHelp=text, longHelp=tooltip_text, kind=kind)
    else:
        kwargs = dict(label=text, bitmap=bmp, bmpDisabled=wx.NullBitmap, shortHelpString=text, longHelpString=tooltip_text, kind=kind)
    return add_tool(wx_ids[text], **kwargs)