import sys


nodes_dict = {}

def mbr_intersects(mbr1, mbr2):

    if mbr1[1] < mbr2[0] or mbr2[1] < mbr1[0]:
        return False

    if mbr1[3] < mbr2[2] or mbr2[3] < mbr1[2]:
        return False

    return True


def range_query(root_id, query_rect):

    result = []
    root_node = nodes_dict[root_id]
    queue = [root_node]

    while queue:
        current_node = queue.pop(0)
        is_non_leaf, node_id, entries = current_node

        for entry in entries:
            entry_id, entry_mbr = entry

            if mbr_intersects(entry_mbr, query_rect):
                if is_non_leaf == 1:
                    child_node = nodes_dict[entry_id]
                    queue.append(child_node)
                else:
                    result.append(entry_id)

    return result


def load_rtree(filename):
    global nodes_dict
    nodes = []
    with open(filename, 'r') as f:
        for line in f:
            node = eval(line.strip())
            nodes.append(node)

    nodes_dict = {node[1]: node for node in nodes}

    root_node = nodes[-1]

    return root_node[1]


def read_queries(filename):

    queries = []
    with open(filename, 'r') as f:
        for line in f:
            coords = [float(x) for x in line.strip().split()]
            if len(coords) == 4:
                query_rect = [coords[0], coords[2], coords[1], coords[3]]
                queries.append(query_rect)
    return queries


if __name__ == "__main__":

    rtree_file = sys.argv[1]
    queries_file = sys.argv[2]

    root_node = load_rtree(rtree_file)

    queries = read_queries(queries_file)

    for i, query_rect in enumerate(queries):
        results = range_query(root_node, query_rect)
        print(f"{i} ({len(results)}): {','.join(map(str, results))}")