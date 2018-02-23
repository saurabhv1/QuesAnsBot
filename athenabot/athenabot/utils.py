def is_number(string):
    if '%' in string:
        string = string.split('%')[0].strip()
    try:
        float(string)
        return True
    except ValueError:
        return False