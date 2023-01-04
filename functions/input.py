import re

def clean_comm(string):
    '''function that takes a command - i.e. a string - and returns the command in a clear and explicit form'''
    string = string.lower()
    try:
        # find the splitting point
        find_capital = re.search(r'(centrality)', string)
        index_capital = find_capital.start()
        string = string[:index_capital].lower() + "_" + string[index_capital:].lower()
    except AttributeError:
        string = string.lower()
        string = string if (string=="pagerank") else (string + "_centrality")
    return(string)
