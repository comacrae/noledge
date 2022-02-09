import json
from os import listdir
from os.path import isfile, join


def get_files(mypath):
    onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f)) and 'json' in f]
    return onlyfiles

def get_json(filepath):
    print(f"FILEPATH: {filepath}")
    with open(filepath, "r") as fp:
        data = json.load(fp)
        return data

def save_json(data,filepath):
    with open(filepath, "w+") as fp:
        json.dump(data,fp)
        return

def change_key_value(data):
    data['content'] =  data['text']
    meta = {'url':data['url']}
    data['meta'] = meta
    data.pop('text')
    data.pop('url')
    return

if __name__ == "__main__":

    files = get_files("./")
    for f in files:
        data = get_json(f)
        change_key_value(data)
        save_json(data,f)

