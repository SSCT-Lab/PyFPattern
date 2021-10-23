@staticmethod
def _output_type_handler(cursor, name, defaultType, length, precision, scale):
    '\n        Called for each db column fetched from cursors. Return numbers as the\n        appropriate Python type.\n        '
    if (defaultType == Database.NUMBER):
        if (scale == (- 127)):
            if (precision == 0):
                outconverter = FormatStylePlaceholderCursor._output_number_converter
            else:
                outconverter = float
        elif (precision > 0):
            outconverter = FormatStylePlaceholderCursor._get_decimal_converter(precision, scale)
        else:
            outconverter = FormatStylePlaceholderCursor._output_number_converter
        return cursor.var(Database.STRING, size=255, arraysize=cursor.arraysize, outconverter=outconverter)