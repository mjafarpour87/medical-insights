from collections import defaultdict
import json
import os
import pathlib
from matplotlib import pyplot as plt
import networkx as nx
import random
import click
from triplea.service.click_logger import logger
from triplea.config.settings import SETTINGS
import json
import pathlib

import click
from config import OUTPUT_DIR


ROOT = pathlib.Path(__file__).resolve().parent.parent


with open(os.path.join(OUTPUT_DIR ,"info.json") ) as json_file:
    data = json.load(json_file)


col = ['Graph Nodes',
     'Graph Edges',
     'Graph Average Degree',
     'Graph Density',
     'Graph Transitivity',
     'Graph Average Clustering Coefficient',
     'Graph Degree Assortativity Coefficient',
     'Graph Radius',
     'Number of Components'
     ]
line = ""
for c in col:
    line = line + "|" + c
line = line + "|"
print(line)

line = ""
for c in col:
    line = line + "|-" 
line = line + "|"
print(line)

for i in data:
    line= ""
    for c in col:
        # print(i.get(c))
        line = line + f"|{i[c]}" 
    line = line + "|"
    print(line)  
