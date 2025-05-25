# import math
#
# import pymorton
#
#
# def find_mbr(coordinates):
#     """Calculate the Minimum Bounding Rectangle for a set of coordinates."""
#     if not coordinates:
#         return None
#
#     min_x = min(coord[0] for coord in coordinates)
#     max_x = max(coord[0] for coord in coordinates)
#     min_y = min(coord[1] for coord in coordinates)
#     max_y = max(coord[1] for coord in coordinates)
#
#     return [min_x, min_y, max_x, max_y]
#
#
# def center_of_mbr(mbr):
#
#     min_x, min_y, max_x, max_y = mbr
#     center_x = (min_x + max_x) / 2
#     center_y = (min_y + max_y) / 2
#
#     return center_x, center_y
#
#
#
#
# # Read all coordinates
# coordinates = []
# with open("coords.txt", 'r') as c:
#     for line in c:
#         line = line.strip()
#         x, y = map(float, line.split(','))
#         coordinates.append((x, y))
#
# # Read all offsets
# offsets = {}
# with open("offsets.txt", 'r') as o:
#     for line in o:
#         line = line.strip().split(',')
#         key = int(line[0])
#         if key not in offsets:
#             offsets[key] = []
#         offsets[key].append(line[1])
#         offsets[key].append(line[2])
#
# # Group coordinates into objects based on offsets
# objects = []
# start_idx = 0
# for offset in offsets:
#     key = int(offset)
#     end_idx = int(offsets[key][1])
#     object_coords = coordinates[start_idx:end_idx]
#     objects.append(object_coords)
#     start_idx = end_idx
#
# # Calculate MBR for each object
# mbrs = []
# mbrs_centers = {}
# z_codes = {}
# for i, obj_coords in enumerate(objects):
#     mbr = find_mbr(obj_coords)
#     mbrs.append(mbr)
#
#     center_x, center_y = center_of_mbr(mbr)
#     z_code = pymorton.interleave_latlng(center_y, center_x)
#
#     z_codes[i] = z_code
#
#     mbrs_centers[i] = center_of_mbr(mbr)
#
#
# z_codes = dict(sorted(z_codes.items(), key=lambda item: item[1]))
#
# print(math.ceil(len(mbrs)/20))
#