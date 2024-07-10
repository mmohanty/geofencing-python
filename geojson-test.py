import json
from shapely.geometry import Point
from shapely.geometry import Polygon

with open("kenya_gps.json", "r") as f:
    kenya_json = json.load(f)

# lame way to get the Nairobi bounding box
for feature in kenya_json['features']:
    if feature['id'] == 0:
        nairobi_bounding_box = feature['geometry']['coordinates']

# The bounding box is a list of lists of points, so we have to unwrap the list with [0]
nairobi_polygon = Polygon(nairobi_bounding_box[0])

# Shapely points are apparently long/lat
cbd_point = Point(36.82052314069416, -1.2832858629766537)
ilri_point = Point(36.722035402975585, -1.2684044950804823)
nakuru_point = Point(36.44850230480384, -0.9135133124309164)

# See: https://shapely.readthedocs.io/en/stable/
print(nairobi_polygon.contains(cbd_point))
print(nairobi_polygon.contains(ilri_point))
print(nairobi_polygon.contains(nakuru_point))