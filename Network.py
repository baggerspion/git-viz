#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
import sys
import LogParse

LOG = []
FILES = {}

def make_pairs():
    pairs = []
    for file in FILES:
        if len(FILES[file]) == 1: continue
        for pos1 in range(len(FILES[file])):
            for pos2 in range(1, len(FILES[file])):
                if pos2 > pos1:
                    pairs.append((FILES[file][pos1], FILES[file][pos2]))
    return pairs

def process_log():
    for entry in LOG:
        if len(entry['files']) == 0:
            continue
        else:
            for file in entry['files']:
                if not file in FILES:
                    FILES[file] = []
                if not entry['author_name'] in FILES[file]:
                    FILES[file].append(entry['author_name'])
    pairs = make_pairs()
    
    # Count how many times this pair was active
    counts = {}
    for pair in pairs:
        if not pair in counts:
            counts[pair] = 0
        counts[pair] += 1

    # Output the pairs
    print("graph G {")
    print("\tsplines = \"true\";")
    print("\toverlap = \"scalexy\";")
    print("\tnode [ style = \"filled\", color = \"#87B09A\", shape = \"circle\", width = \"0.1\", fixedsize = \"true\", label = \"\" ];")
    for count in counts:
        print("\t\"%s\" -- \"%s\" [ weight = \"%s\" ];" %
              (count[0], count[1], counts[count])
              )
    print("}")

if __name__ == '__main__':
    parser = LogParse.LogParse(sys.argv[1])
    LOG = parser.get_log()
    process_log()
