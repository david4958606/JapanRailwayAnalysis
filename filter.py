import networkx as nx
from plot import *


def filter_degree(G, degree):
    G_filtered = G.copy()
    for node in list(G.nodes):
        if G.degree(node) <= degree:
            G_filtered.remove_node(node)
    return G_filtered


def filter_top_nodes(G, top):
    degree_dict = dict(G.degree())
    degree_dict = dict(sorted(degree_dict.items(), key=lambda x: x[1], reverse=True))
    top_nodes = list(degree_dict.keys())[:top]
    G_filtered = G.subgraph(top_nodes)
    return G_filtered


if __name__ == "__main__":
    # Define parameters
    graph_file = 'jr_graph.pkl'
    min_degree = 2
    top = 100
    graph_file_filtered = 'jr_graph_filtered.pkl'
    # Load graph
    G = load_graph(graph_file)
    print("Network Loaded")
    # Filter graph
    # G_filtered = filter_degree(G, min_degree)
    # print(f"Nodes with degree <= {min_degree} removed")
    G_filtered = filter_top_nodes(G, top)
    print(f"Top {top} nodes kept")
    # Save filtered graph
    save_graph(G_filtered, graph_file_filtered)
    print("Filtered graph saved")
    # Output the new graph to csv
    nx.write_edgelist(G_filtered, "jr_graph_filtered.csv", delimiter=",")
    print("Filtered graph saved as csv")
    # Visualize filtered graph
    # visualize_graph(G_filtered, 'jr_graph_filtered.png')
    # print("Filtered graph visualized")
