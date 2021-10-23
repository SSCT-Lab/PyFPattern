@cached_property
def function_names(self):
    return ({
        'Length': 'GLength',
    } if self.is_mysql_5_5 else {
        
    })