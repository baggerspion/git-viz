#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import LogParse
import argparse
import operator
import sys

from datetime import datetime
from graphviz import Graph

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

    # Create the graph
    g = Graph(engine = "neato", format="png")
    g.graph_attr['splines'] = "true"
    g.graph_attr['overlap'] = "scalexy"
    g.node_attr={
        'style': "filled",
        'color': "#87B09A", 
        'shape': "circle", 
        'width': "0.1", 
        'fixedsize': "true", 
        'label': ""
        }
    for count in counts:
        g.edge(count[0], count[1], weight = str(counts[count]))

    # Write it out
    g.render("result")

if __name__ == '__main__':
    # Parse the args before all else
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("path", help = "Path of the Git repostory to process.")
    arg_parser.add_argument("-f", "--start", help = "Start date")
    arg_parser.add_argument("-u", "--end", help = "End date")
    args = arg_parser.parse_args()

    log_parser = LogParse.LogParse(args.path)
    if not (args.start and args.end):
        LOG = log_parser.get_log()
    else:
        LOG = log_parser.get_log(args.start, args.end)
    process_log()
