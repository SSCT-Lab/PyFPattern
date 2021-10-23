@staticmethod
def _output_type_handler(cursor, name, defaultType, length, precision, scale):
    "\n        Called for each db column fetched from cursors. Return numbers as\n        strings so that decimal values don't have rounding error.\n        "
    if (defaultType == Database.NUMBER):
        return cursor.var(Database.STRING, size=255, arraysize=cursor.arraysize, outconverter=str)