import logging

from datetime import datetime
import numpy as np
import networkx as nx
import math
import pandas as pd
import matplotlib.pyplot as plt
import os
import pathlib
import copy

if __name__ == "__main__":

    with open("dataset_10335_10ans.txt") as f:
        data = f.read().splitlines()

        s = int(data[0])
        d = data[1:]

    G = nx.Graph()

    for line in d:
        vals = line.replace("->", ":").split(":")
        G.add_edge(vals[0], vals[1], dist=vals[2])

    ## draw graph boilerplate ##
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=True)

    # pos_off = copy.deepcopy(pos)
    # for k in pos_off.keys():
    #     pos_off[k] = pos_off[k] + 0.08
    # node_labels = nx.get_node_attributes(G, "age")
    # nx.draw_networkx_labels(G, pos_off, labels=node_labels)

    edge_labels = nx.get_edge_attributes(G, "dist")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    p = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs", "graph%s.png" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
    plt.savefig(p)
    plt.clf()
    ## end graph ##

    ## logger boilerplate ##
    logger = logging.getLogger(__name__)

    logdir = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs")
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    f = os.path.join(logdir, "log_%s.log" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
    f_handler = logging.FileHandler(f)
    f_format = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s: %(message)s")
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

    logging.getLogger().setLevel(logging.DEBUG)
    logger.debug("test debug message")
    logger.info("test info message")
    logger.warning("test warning message")
    logger.error("test error message")
    ## end logger ##
