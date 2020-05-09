

def drop_record_decorator(function):
    def drop_record_id(result):
        return result.reset_index('Record ID', drop=True)
    @functools.wraps(function)
    def wrapper(result):
        result = function(result)
        result = drop_record_id(result)
        return result
    return wrapper

def result_decorator(calculate_func):
    @functools.wraps(calculate_func)
    def wrapper(result:pd.Series) -> pd.DataFrame:
        result =calculate_func(result)
        df = get_result(result)
        return df
    return wrapper
