import pandas as pd
import json
from os import listdir 
from os.path import isfile, join


def get_only_files(dirpath):
    return [ f for f in listdir(dirpath) if isfile(join(dirpath, f)) and '.json' in f ]


def json_to_csv(dirpath,filename):
    path = str(join(dirpath, filename))
    with open(path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        if 'document_text' not in data.keys():
            data['document_text'] = data.pop('text')
        df = pd.json_normalize(data)
        df.to_csv(path.replace('.json','.csv'), index=False, encoding='utf-8')
    return

if __name__ == "__main__":

    files = get_only_files(".")
    print(type(files))
    print(type(files[0]))
    for f in files:
        json_to_csv(".", f)

