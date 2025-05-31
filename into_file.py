#! /usr/bin/env python3
from os import walk, path
from sys import argv
import json

def get(l, index, default):
    return l[index] if index < len(l) else default

def rec_get(dic, parts):
    for part in parts:
        dic = dic[part]
    return dic

def make_structure(profile):
    out = {}
    for (dirpath, _, filenames) in walk(profile):
        (*paths, this) = dirpath.split("/")
        parent = rec_get(out, paths)
        parent[this] = {}
        loc = parent[this]
        for filename in filenames:
            with open(path.join(*paths, this, filename), 'r') as file:
                link = file.readline().strip()
            loc[filename] = link
    return out[profile]

# format in firefox-able bookmarks html
def format_html(struct, ident=""):
    """
    {
        "reads": {
            "fireborn": "https://fireborn.mataroa.blog/"
        }
    }
    ->
    "<DL>
        <DT><H3>reads</H3>
        <DL>
                <DT><A HREF="https://fireborn.mataroa.blog/">fireborn</A>
        </DL>
    </DL>"
    """
    print(f"{ident}<DL>")

    for (k, v) in struct.items():
        if type(v) == str:
            print(f'{ident}  <DT><A HREF="{v}">{k}</A>')
        else:
            print(f"{ident}  <DT><H3>{k}</H3>")
            format_html(v, ident+"  ")

    print(f"{ident}</DL>")

def main():
    profile = get(argv, 1, "personal")
    out_type = get(argv, 2, "html")
    out = make_structure(profile)

    if out_type == "json":
        print(json.dumps(out))
    elif out_type == "html":
        format_html(out)


if __name__ == "__main__":
    main()
