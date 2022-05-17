def sanitize(input):
    # Dictionary of bad characters to be removed and replaced
    bad = {'=': '', '%': '', '\'': '', '\"': '', '\\': '', '/': ''}
    
    for i, j in bad.items():
        input = input.replace(i, j)
    
    return input