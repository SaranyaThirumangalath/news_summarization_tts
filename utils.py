import json

def pretty_print_json(data, indent=2):
    """
    Converts a dictionary or list to a pretty-formatted JSON string.
    
    Parameters:
        data (dict or list): The data to format.
        indent (int): The number of spaces for indentation (default is 2).
    
    Returns:
        str: A JSON string with indentation for easier reading.
        
    Example:
        my_dict = {"name": "Tesla", "status": "Active"}
        print(pretty_print_json(my_dict))
    """
    # json.dumps converts the data to a JSON-formatted string.
    # 'ensure_ascii=False' preserves Unicode characters.
    return json.dumps(data, indent=indent, ensure_ascii=False)

def safe_get(d, key, default=None):
    """
    Safely retrieves the value for a given key from a dictionary.
    If the key does not exist or if d is not a dictionary, returns the default value.
    
    Parameters:
        d (dict): The dictionary from which to get the value.
        key (str): The key to look for.
        default: The default value to return if the key is missing (default is None).
    
    Returns:
        The value associated with the key if it exists, otherwise the default value.
    
    Example:
        my_dict = {"name": "Tesla"}
        print(safe_get(my_dict, "name", "Unknown"))   # Output: Tesla
        print(safe_get(my_dict, "status", "Unknown")) # Output: Unknown
    """
    try:
        return d.get(key, default)
    except AttributeError:
        # If d is not a dictionary, return the default value.
        return default