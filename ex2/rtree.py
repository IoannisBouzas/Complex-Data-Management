import math
import sys
import pymorton


def find_mbr(coordinates):

    if not coordinates:
        return None

    min_x = min(coord[0] for coord in coordinates)
    max_x = max(coord[0] for coord in coordinates)
    min_y = min(coord[1] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    return [min_x, max_x, min_y, max_y]


def center_of_mbr(mbr):

    min_x, max_x, min_y, max_y = mbr
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    return center_x, center_y


def combine_mbrs(mbrs):

    if not mbrs:
        return None

    min_x = min(mbr[0] for mbr in mbrs)
    max_x = max(mbr[1] for mbr in mbrs)
    min_y = min(mbr[2] for mbr in mbrs)
    max_y = max(mbr[3] for mbr in mbrs)

    return [min_x, max_x, min_y, max_y]


def distribute_entries(entries, node_capacity, min_entries):

    if len(entries) <= node_capacity:
        return [entries]

    total_entries = len(entries)

    num_nodes = math.ceil(total_entries / node_capacity)

    last_node_entries = total_entries % node_capacity
    if last_node_entries == 0:
        last_node_entries = node_capacity

    if last_node_entries < min_entries and num_nodes > 1:

        entries_per_node = math.floor((total_entries - min_entries) / (num_nodes - 1))

        if entries_per_node > node_capacity:
            nodes = []
            for i in range(0, total_entries, node_capacity):
                end = min(i + node_capacity, total_entries)
                nodes.append(entries[i:end])
            return nodes

        nodes = []
        start = 0
        for i in range(num_nodes - 1):
            end = start + entries_per_node
            nodes.append(entries[start:end])
            start = end

        nodes.append(entries[start:])

        return nodes
    else:
        nodes = []
        for i in range(0, total_entries, node_capacity):
            end = min(i + node_capacity, total_entries)
            nodes.append(entries[i:end])
        return nodes


def build_rtree(entries, start_node_id=0, node_capacity=20, min_entries=8):

    if len(entries) <= node_capacity:
        return [[0, start_node_id, entries]], start_node_id + 1


    distributed_entries = distribute_entries(entries, node_capacity, min_entries)
    #nodes = []
    node_id = start_node_id

    leaf_nodes = []
    for node_entries in distributed_entries:
        leaf_nodes.append([0, node_id, node_entries])
        node_id += 1

    parent_entries = []
    for leaf_node in leaf_nodes:
        isnonleaf, leaf_id, leaf_entries = leaf_node
        mbrs = [entry[1] for entry in leaf_entries]
        node_mbr = combine_mbrs(mbrs)
        parent_entries.append([leaf_id, node_mbr])

    upper_nodes, next_node_id = build_rtree(parent_entries, node_id, node_capacity, min_entries)

    for node in upper_nodes:
        node[0] = 1

    return leaf_nodes + upper_nodes, next_node_id


def count_nodes_by_level(nodes):

    node_map = {node[1]: node for node in nodes}

    children = set()
    for node in nodes:
        if node[0] == 1:
            for entry in node[2]:
                children.add(entry[0])

    root_id = next((node[1] for node in nodes if node[1] not in children), nodes[0][1])

    queue = [(root_id, 0)]
    levels = {root_id: 0}

    for node_id, level in queue:
        node = node_map[node_id]
        if node[0] == 1:
            for entry in node[2]:
                child_id = entry[0]
                levels[child_id] = level + 1
                queue.append((child_id, level + 1))

    level_counts = {}
    for level in levels.values():
        level_counts[level] = level_counts.get(level, 0) + 1

    max_level = max(levels.values()) if levels else 0

    return level_counts, max_level, root_id

def main():

    coords_file = sys.argv[1]
    offsets_file = sys.argv[2]

    coordinates = []
    with open(coords_file, 'r') as c:
        for line in c:
            line = line.strip()
            if line:
                x, y = map(float, line.split(','))
                coordinates.append((x, y))

    offsets = {}
    with open(offsets_file, 'r') as o:
        for line in o:
            line = line.strip().split(',')
            if len(line) >= 3:
                obj_id = int(line[0])
                start_offset = int(line[1])
                end_offset = int(line[2])
                offsets[obj_id] = (start_offset, end_offset)

    objects = {}
    for obj_id, (start_offset, end_offset) in offsets.items():
        objects[obj_id] = coordinates[start_offset:end_offset]

    mbrs = {}
    z_codes = {}

    for obj_id, obj_coords in objects.items():
        mbr = find_mbr(obj_coords)
        mbrs[obj_id] = mbr

        center_x, center_y = center_of_mbr(mbr)
        z_code = pymorton.interleave_latlng(center_y, center_x)
        z_codes[obj_id] = z_code

    sorted_ids = sorted(z_codes.keys(), key=lambda obj_id: z_codes[obj_id])

    leaf_entries = [[obj_id, mbrs[obj_id]] for obj_id in sorted_ids]

    node_capacity = 20
    min_entries = int(0.4 * node_capacity)
    rtree_nodes, _ = build_rtree(leaf_entries, 0, node_capacity, min_entries)

    level_counts, max_level, root_id = count_nodes_by_level(rtree_nodes)


    for level in range(max_level, -1, -1):
        inverted_level = max_level - level
        count = level_counts.get(level, 0)
        if count == 1:
            print(f"{count} node at level {inverted_level}")
        else:
            print(f"{count} nodes at level {inverted_level}")

    rtree_nodes.sort(key=lambda node: 0 if node[1] == root_id else node[1])


    for i, node in enumerate(rtree_nodes):
        if node[1] == root_id:
            rtree_nodes.append(rtree_nodes.pop(i))
            break


    with open("Rtree.txt", 'w') as f:
        for node in rtree_nodes:
            f.write(str(node) + '\n')


if __name__ == "__main__":
    main()