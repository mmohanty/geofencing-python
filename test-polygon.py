import json
from shapely.geometry import Point, MultiPolygon, shape, Polygon

MAP = dict()


def load_data():
    # Opening JSON file
    f = open('us-states.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for feature in data['features']:
        MAP.__setitem__(int(feature['id']), feature['geometry'])

    # Closing file
    f.close()


def point_in_polygon(point, polygon):

    point_shapely = Point(point[0], point[1])
    polygon_shapely = Polygon(polygon)
    return polygon_shapely.contains(point_shapely)


def point_in_multipolygon(point, geometry):

    # Load GeoJSON as a Shapely geometry
    #polygon = shape(geometry)
    polygon = MultiPolygon(geometry['coordinates'])

    # Check if the point is within the MultiPolygon
    is_within = polygon.contains(point)

    if is_within:
        return True
    else:
        return False


if __name__ == '__main__':
    # Example 1 usage
    # point = [2, 5]
    # multipolygon = [
    #     [[0, 0], [5, 0], [5, 10], [0, 10]],
    #     [[3, 3], [7, 3], [7, 7], [3, 7]]
    # ]
    #
    # if point_in_multipolygon(point, multipolygon):
    #     print("Point is inside at least one polygon")
    # else:
    #     print("Point is outside all polygons")
    #
    # # Example 2 usage
    # point = [2, 5]
    # polygon = [[0, 0], [5, 0], [5, 10], [0, 10]]
    #
    # if point_in_polygon(point, polygon):
    #     print("Point is inside the polygon")
    # else:
    #     print("Point is outside the polygon")

    #Example 3
    load_data()
    feature_id = '02'
    geometry_type = MAP.get(int(feature_id))['type']
    geometry = MAP.get(int(feature_id))
    if geometry_type == 'MultiPolygon':
        print('MultiPolygon')
        bounding_boxes = geometry['coordinates']

        polygons = []
        for bounding_box in bounding_boxes:
            # The bounding box is a list of lists of points, so we have to unwrap the list with [0]
            feature_polygon = Polygon(bounding_box[0])
            polygons.append(feature_polygon)

        # Shapely points are apparently long/lat (Alaska)
        cbd_point = Point(-134.433304, 58.305801)
        flag = False
        for poly in polygons:
            if poly.contains(cbd_point):
                flag = True
                break
            else:
                continue
        print(flag)

    if geometry_type == 'Polygon':
        print('Polygon')
        bounding_box = geometry['coordinates']
        # The bounding box is a list of lists of points, so we have to unwrap the list with [0]
        feature_polygon = Polygon(bounding_box[0])
        # Shapely points are apparently long/lat (Alabama)
        cbd_point = Point(-86.75558745272863, 32.90976397557229)
        print(feature_polygon.contains(cbd_point))

