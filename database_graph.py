import json

import networkx as nx
import matplotlib.pyplot as plt
import argparse


def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def build_network(data):
    G = nx.Graph()

    for dest_url, sources in data.items():
        for source_url, weight in sources.items():
            G.add_edge(source_url, dest_url, weight=weight)

    edgewidth = [d['weight'] for (u, v, d) in G.edges(data=True)]
    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=80)
    nx.draw_networkx_edges(G, pos, width=edgewidth)
    plt.axis('off')
    image = 'network.png'
    plt.savefig(image)
    return image


def parse_args():
    parser = argparse.ArgumentParser(description='Visualize data')
    parser.add_argument('--filename', help='data file', required=True)
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    args = parse_args()
    filename = args['filename']
    data = load_data(filename)
    build_network(data)
