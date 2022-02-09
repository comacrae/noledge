import json
import os

def get_filenames(dirpath):
    files = [f for f in os.listdir(dirpath) if'.json' in f]
    return files

def json_to_txt(dirpath, filename):
    with open(os.path.join(dirpath,filename), 'r') as f:
        contents = json.load(f)['text']
        f.close()
    return contents

def write_file(dirpath, filename,contents):
    filename = filename.replace('.json', '.txt')
    with open(os.path.join(dirpath, filename), 'w+') as f:
        f.write(contents)
        f.close()
    return
        

if __name__ == "__main__":
    d = '.'
    files = get_filenames(d) 
    for f in files:
        c = json_to_txt(d, f)
        write_file(d, f, c)

