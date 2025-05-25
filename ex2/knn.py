import sys
import heapq
import math


nodes_dict = {}
query_point = None
k = None


def mindist(point, mbr):

    x, y = point
    x_min, x_max, y_min, y_max = mbr


    closest_x = max(x_min, min(x, x_max))
    closest_y = max(y_min, min(y, y_max))


    dx = x - closest_x
    dy = y - closest_y

    return math.sqrt(dx * dx + dy * dy)


def knn_search(root_id):

    global nodes_dict, query_point, k

    root_node = nodes_dict[root_id]

    pq = []
    result = []

    is_non_leaf, node_id, entries = root_node

    for entry_id, entry_mbr in entries:

        dist = mindist(query_point, entry_mbr)

        heapq.heappush(pq, (dist, entry_id, entry_mbr, is_non_leaf != 1))

    while pq and len(result) < k:

        dist, entry_id, entry_mbr, is_object = heapq.heappop(pq)

        if is_object:

            result.append(entry_id)
        else:

            node = nodes_dict[entry_id]
            is_non_leaf, node_id, entries = node

            for child_id, child_mbr in entries:
                child_dist = mindist(query_point, child_mbr)

                heapq.heappush(pq, (child_dist, child_id, child_mbr, is_non_leaf != 1))

    return result


def get_root_id(rtree):

    with open(rtree, 'r') as f:
        lines = f.readlines()
        root_node = eval(lines[-1].strip())
        _, root_id, _ = root_node
    return root_id


def process_knn_queries(rtree, queries, k_value):

    global nodes_dict, k
    k = k_value

    nodes_dict = {}
    with open(rtree, 'r') as f:
        for line in f:
            node = eval(line.strip())
            is_non_leaf, node_id, entries = node
            nodes_dict[node_id] = node


    root_id = get_root_id(rtree)

    with open(queries, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):

        cords = line.strip().split()

        try:
            global query_point

            x, y = map(float, cords)
            query_point = [x, y]


            results = knn_search(root_id,)

            print(f"{i} ({len(results)}):", end=" ")
            print(*results, sep=",")

        except:
            continue


if __name__ == "__main__":

    rtree = sys.argv[1]
    queries = sys.argv[2]
    k = int(sys.argv[3])


    process_knn_queries(rtree, queries, k)

