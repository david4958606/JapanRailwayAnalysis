import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import pickle


# 加载JSON数据
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 创建图
def create_graph_from_line(lines_data):
    G = nx.Graph()

    for line_info in lines_data:
        line = line_info['line']
        stations = line_info['stations']

        # 为每条线路添加节点和边
        for i in range(len(stations) - 1):
            station_a = stations[i]
            station_b = stations[i + 1]
            G.add_edge(station_a, station_b, line=line)

    return G


# 从车站数据创建图，每个车站是一个节点，相邻车站之间的连接是一条边
def create_graph_from_stations(stations_data):
    G = nx.Graph()

    for station_info in stations_data:
        station = station_info['name']
        neighbors = station_info['neighbors']

        # 为每个车站添加节点和边
        for neighbor in neighbors:
            neighbor_name = neighbor['name']
            distance = neighbor['distance']
            G.add_edge(station, neighbor_name, distance=distance)

    return G


def create_graph_form_csv(csv_file):
    df = pd.read_csv(csv_file)
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row['station_name_1'], row['station_name_2'], line_name=row['line_name'])
    return G


def create_weighted_graph_form_csv(csv_file):
    df = pd.read_csv(csv_file)
    G = nx.Graph()
    for _, row in df.iterrows():
        station1 = row['station_name_1']
        station2 = row['station_name_2']
        if G.has_edge(station1, station2):
            G[station1][station2]['weight'] += 1
        else:
            G.add_edge(station1, station2, weight=1)
    return G


# 保存图到文件
def save_graph(G, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(G, f)


# 从文件加载图
def load_graph(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


# 可视化图并保存到文件
def visualize_graph(G, output_file, size=100, dpi=300):
    plt.figure(figsize=(size, size))  # 增大图像尺寸以提高分辨率
    pos = nx.spring_layout(G)  # 使用弹簧布局

    # Fix japanese font
    plt.rc('font', family='Yu Gothic')

    # 绘制节点和边
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='blue', alpha=0.6)
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='Yu Gothic')

    plt.title('JR Lines Visualization')
    plt.axis('off')
    plt.savefig(output_file, format='png', dpi=dpi)  # 保存为文件，设置较高的DPI以提高分辨率
    plt.close()

def visualize_weighted_graph(G, output_file, size=20, dpi=300, title="Title", layout='spring', seed=42):
    plt.figure(figsize=(size, size))
    if layout == 'spring':
        pos = nx.spring_layout(G, seed=seed)
    elif layout == 'kamada':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    else:
        pos = nx.shell_layout(G)

    # Fix japanese font
    plt.rc('font', family='Yu Gothic')

    # 绘制节点和边
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='blue', alpha=0.6)
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='Yu Gothic')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_family='Yu Gothic')

    plt.title(title)
    plt.axis('off')
    plt.savefig(output_file, format='png', dpi=dpi)  # 保存为文件，设置较高的DPI以提高分辨率
    plt.close()
