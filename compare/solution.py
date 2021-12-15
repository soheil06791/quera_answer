def compare(string1, string2):
    ali_str = list(string1)
    salib_str = list(string2)
    while ali_str and salib_str:
        print(ali_str,salib_str)
        if ali_str[0] < salib_str[0]:
            del ali_str[0]
            ali_str = ali_str[::-1]
            salib_str = salib_str[::-1]
        elif ali_str[0] > salib_str[0]:
            del salib_str[0]
            salib_str = salib_str[::-1]
            ali_str = ali_str[::-1]
        else:
            del ali_str[0]
            del salib_str[0]
            salib_str = salib_str[::-1]
            ali_str = ali_str[::-1]
    if ali_str:
        return ''.join(ali_str[::-1])
    elif salib_str:
        return ''.join(salib_str[::-1])
    else:
        return 'Both strings are empty!'

