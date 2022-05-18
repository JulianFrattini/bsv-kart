GLOBAL_SALE = 10
VERSION = 1

def get_global_variable(identifier: str):
    """Obtain the global value associated to the given identifier.

    returns
        value -- value associated to the identifier
        None -- if no value is associated to that identifier    
    """
    if identifier.lower() in ['version', 'v']:
        return VERSION
    elif identifier.lower() in ["global_sale", "global sale"]:
        return GLOBAL_SALE
    return None