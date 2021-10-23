@cached_property
def function_names(self):
    return {
        'Area': ('Area' if self.is_mysql_5_5 else 'ST_Area'),
        'Centroid': ('Centroid' if self.is_mysql_5_5 else 'ST_Centroid'),
        'Difference': 'ST_Difference',
        'Distance': 'ST_Distance',
        'Envelope': ('Envelope' if self.is_mysql_5_5 else 'ST_Envelope'),
        'Intersection': 'ST_Intersection',
        'Length': ('GLength' if self.is_mysql_5_5 else 'ST_Length'),
        'NumGeometries': ('NumGeometries' if self.is_mysql_5_5 else 'ST_NumGeometries'),
        'NumPoints': ('NumPoints' if self.is_mysql_5_5 else 'ST_NumPoints'),
        'SymDifference': 'ST_SymDifference',
        'Union': 'ST_Union',
    }