def get_current_function(connection, function_name, qualifier=None):
    try:
        if (qualifier is not None):
            return connection.get_function(FunctionName=function_name, Qualifier=qualifier)
        return connection.get_function(FunctionName=function_name)
    except ClientError:
        return None