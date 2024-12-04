import networkx as nx
import community.community_louvain as community_louvain
from infomap import Infomap
from collections import Counter
import json


def find_max_degree_node(G):
    # 使用 NetworkX 提供的 degree() 函数来获取每个节点的度
    max_node, max_degree = max(G.degree, key=lambda x: x[1])
    return max_node, max_degree


def find_degree(G, node):
    return G.degree(node)


def find_shortest_path(G, start, end):
    shortest_path = nx.shortest_path(G, source=start, target=end)

    return shortest_path


def find_all_path(G, start, end):
    all_paths = list(nx.all_simple_paths(G, source=start, target=end))

    return len(all_paths)


def get_neighbors(G, node):
    return list(G.neighbors(node))


def check_node_exists(G, node):
    return G.has_node(node)


def find_communities(G):
    # 使用 Louvain 方法来计算社区
    partition = community_louvain.best_partition(G)
    return partition


def find_largest_community(G):
    # 使用 Louvain 方法来计算社区
    partition = community_louvain.best_partition(G)

    # 统计每个社区的节点数量
    community_counter = Counter(partition.values())

    # 找到节点数量最多的社区
    largest_community_id = max(community_counter, key=community_counter.get)

    # 找到属于最大社区的节点
    largest_community_nodes = [node for node, community in partition.items(
    ) if community == largest_community_id]

    return largest_community_id, largest_community_nodes


def find_smallest_community(G):
    # 使用 Louvain 方法来计算社区
    partition = community_louvain.best_partition(G)

    # 统计每个社区的节点数量
    community_counter = Counter(partition.values())

    # 找到节点数量最少的社区
    smallest_community_id = min(community_counter, key=community_counter.get)

    # 找到属于最小社区的节点
    smallest_community_nodes = [node for node, community in partition.items(
    ) if community == smallest_community_id]

    return smallest_community_id, smallest_community_nodes

def find_all_communities(G):
    # 使用 Louvain 方法来计算社区
    partition = community_louvain.best_partition(G)

    # 统计每个社区的节点数量
    community_counter = Counter(partition.values())

    comm_dict = {} # key: community_id, value: nodes in the community
    for node, community in partition.items():
        if community in comm_dict:
            comm_dict[community].append(node)
        else:
            comm_dict[community] = [node]

    return comm_dict

def infomap_community(G):
    im = Infomap("--two-level --directed")
    for u, v, data in G.edges(data=True):
        weight = data['weight'] if 'weight' in data else 1
        im.add_link(u, v, weight)
    im.run()
    print("社区划分结果:")
    for node_id, module_id in im.modules.items():
        print(f"节点 {node_id} 属于社区 {module_id}")


# dict to json
def dict_to_json(data_dict):
    """
    Converts a Python dictionary to a JSON string.
    
    Args:
        data_dict (dict): The dictionary to convert.
    
    Returns:
        str: The JSON string representation of the dictionary.
    """
    try:
        # 将字典转换为JSON字符串，确保中文字符显示为正常文本
        json_str = json.dumps(data_dict, ensure_ascii=False, indent=4)
        return json_str
    except Exception as e:
        print(f"Error converting dictionary to JSON: {e}")
        return None
