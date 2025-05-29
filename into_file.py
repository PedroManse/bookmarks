from os import walk, path
from sys import argv
import json
out = {}

def get(l, index, default):
    return l[index] if index < len(l) else default
    

def rec_get(dic, parts):
    for part in parts:
        dic = dic[part]
    return dic

for (dirpath, _, filenames) in walk(get(argv, 1, ".")):
    (*paths, this) = dirpath.split("/")
    parent = rec_get(out, paths)
    parent[this] = {}
    loc = parent[this]
    for filename in filenames:
        with open(path.join(*paths, this, filename), 'r') as file:
            link = file.readline().strip()
        loc[filename] = link

print(json.dumps(out[get(argv, 1, ".")]))
