def json_loader(_filename):
    with open(_filename, 'r') as fp:
        data = fp.read()
        fp.close()
    return data
