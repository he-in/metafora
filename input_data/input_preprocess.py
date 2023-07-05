import fiona
import shapefile as shp
import networkx as nx


def gen_nodes_from_roads(roads_fullpath, nodes_output_fullpath):
    nodes_list = list()
    node_id = 0
    link_sf = shp.Reader(roads_fullpath)

    for record in link_sf.shapeRecords():
        for i in [0, -1]:
            point = record.shape.points[i]
            pt = (round(point[0], 6), round(point[1], 6))
            if pt not in nodes_list:
                nodes_list.append((round(point[0], 6), round(point[1], 6)))

    print("nodes list first pass")
    nodes_list = list(set(nodes_list))
    print("removed duplicates")
    schema = {
        'geometry': 'Point',
        'properties': [('ID', 'str')]
    }

    pointShp = fiona.open(nodes_output_fullpath, mode='w', driver='ESRI Shapefile',
                          schema=schema, crs="EPSG:4326")

    for node in nodes_list:
        node_id = node_id + 1
        digits = len(str(node_id))
        if digits < 2:
            node_id_str = "0" * 5 + str(node_id)
        elif digits < 3:
            node_id_str = "0" * 4 + str(node_id)
        elif digits < 4:
            node_id_str = "0" * 3 + str(node_id)
        elif digits < 5:
            node_id_str = "0" * 2 + str(node_id)
        elif digits < 6:
            node_id_str = "0" * 1 + str(node_id)
        else:
            node_id_str = str(node_id)

        nodeDict = {
            'geometry': {'type': 'Point',
                         'coordinates': node},
            'properties': {'ID': node_id_str},
        }
        pointShp.write(nodeDict)

    pointShp.close()
    return nodes_list


def gen_links_from_roads(nodes_fullpath, roads_fullpath, links_output_fullpath, nodes_list):
    links_list = []
    links_id_list = []
    mainkey_list = []
    link_id = 0
    ind = 0

    if not nodes_list:
        node_sf = shp.Reader(nodes_fullpath)
        nodes_list = []
        for record in node_sf.shapeRecords():
            nodes_list.append((record.shape.points[0][0], record.shape.points[0][1]))
    # road_type_list = ['seconary','motorway', 'residential', 'primary', 'primary_link', 'trunk', 'tertiary']

    nodes_list = list(set(nodes_list))  # remove duplicates

    roads_sf = shp.Reader(roads_fullpath)

    print('checking nodes to make links')

    not_wanted_list = [20010, 20014, 20019, 20017, 20012, 20013]
    for record in roads_sf.shapeRecords():
        if record.record.mainkey not in not_wanted_list:
            if record.record.mainkey == 20014:
                print("wtf")
            p0 = (record.shape.points[0][0], record.shape.points[0][1])
            p1 = (record.shape.points[-1][0], record.shape.points[-1][1])
            intermediate_points = []
            if len(record.shape.points) > 2:
                for pt in record.shape.points[1:-1]:
                    pt_round = (round(pt[0], 6), round(pt[1], 6))
                    if pt_round in nodes_list:  # for efficiency
                        intermediate_points.append(pt)

            if len(intermediate_points) > 0:
                intermediate_points = sorted(set(intermediate_points), key=lambda x: intermediate_points.index(x))
                intermediate_points = [p0] + intermediate_points + [p1]
                # print("cut a big link")
                # a_id = 97
                for ind, ip in enumerate(intermediate_points):
                    if ind > 0:
                        pts_list = record.shape.points
                        fractioned_link = pts_list[pts_list.index(intermediate_points[ind - 1]): len(pts_list) - pts_list[
                                                                                                                 ::-1].index(
                            intermediate_points[ind])]
                        actual_link = []
                        for p in fractioned_link:
                            new_p = (round(p[0], 6), round(p[1], 6))
                            actual_link.append(new_p)
                        reversed_link = list(reversed(actual_link))
                        if not actual_link:
                            print("empty actual link")
                        if actual_link not in links_list and reversed_link not in links_list:
                            links_list.append(actual_link)
                            links_id_list.append(str(record.record.ID_1))
                            mainkey_list.append(str(record.record.mainkey))
                            # links_id_list.append(str(record.record.ID_1)+chr(a_id).encode('utf-8').decode('utf-8'))
                            # e = 1
                            # a_id = a_id + 1
            else:
                actual_link = []
                for p in record.shape.points:
                    new_p = (round(p[0], 6), round(p[1], 6))
                    actual_link.append(new_p)
                reversed_link = list(reversed(actual_link))
                if not actual_link:
                    print("empty actual link")
                if actual_link not in links_list and reversed_link not in links_list:
                    links_list.append(actual_link)
                    links_id_list.append(str(record.record.ID_1))
                    mainkey_list.append(str(record.record.mainkey))
                    # e = 1

    print('Made lots of links.')
    print('The length of links_list is :' + str(len(links_list)))
    print('The length of links_id_list is :' + str(len(links_id_list)))

    schema = {
        'geometry': 'LineString',
        'properties': [('ID', 'str'), ('ID_python', 'str'), ('ID_1', 'str'), ('mainkey', 'str')]
    }

    link_shp = fiona.open(links_output_fullpath, mode='w', driver='ESRI Shapefile',
                          schema=schema, crs="EPSG:4326")

    for link in links_list:
        link_id = link_id + 1
        digits = len(str(link_id))
        if digits < 2:
            link_id_str = "0" * 5 + str(link_id)
        elif digits < 3:
            link_id_str = "0" * 4 + str(link_id)
        elif digits < 4:
            link_id_str = "0" * 3 + str(link_id)
        elif digits < 5:
            link_id_str = "0" * 2 + str(link_id)
        elif digits < 6:
            link_id_str = "0" * 1 + str(link_id)
        else:
            link_id_str = str(link_id)

        # print(ind)
        # print(links_id_list[ind])


        link_dict = {
            'geometry': {'type': 'LineString',
                         'coordinates': link},
            'properties': {'ID': link_id_str,
                           'ID_python': link_id_str,
                           'ID_1': links_id_list[links_list.index(link)],
                           'mainkey': mainkey_list[links_list.index(link)]},
        }
        link_shp.write(link_dict)

        ind = ind + 1

    link_shp.close()


def gen_strongest_network(nodes_fullpath, links_fullpath, nodes_strongest_fullpath, links_strongest_fullpath):
    # graph = nx.MultiDiGraph()
    graph = nx.MultiGraph()
    links_sf = shp.Reader(links_fullpath)
    nodes_sf = shp.Reader(nodes_fullpath)
    edges_list = []

    for rec in nodes_sf.shapeRecords():
        e = 0

    for record in links_sf.shapeRecords():
        edges_list.append((record.shape.points[0], record.shape.points[-1]))
    graph.add_edges_from(edges_list)
    # largest = max(nx.strongly_connected_components(graph), key=len)
    largest = max(nx.connected_components(graph), key=len)

    line_schema = {
        'geometry': 'LineString',
        'properties': [('ID', 'str'), ('ID_python', 'str'), ('ID_1', 'str'), ('mainkey', 'str')]
    }

    link_shp = fiona.open(links_strongest_fullpath, mode='w', driver='ESRI Shapefile',
                          schema=line_schema, crs="EPSG:4326")

    for record in links_sf.shapeRecords():
        if record.shape.points[0] in largest and record.shape.points[-1] in largest:
            link_dict = {
                'geometry': {'type': 'LineString',
                             'coordinates': record.shape.points},
                'properties': {'ID': record.record.ID,
                               'ID_python': record.record.ID_python,
                               'ID_1': record.record.ID_1,
                               'mainkey': record.record.mainkey
                               },
            }
            link_shp.write(link_dict)

    link_shp.close()

    node_schema = {
        'geometry': 'Point',
        'properties': [('ID', 'str')]
    }

    point_shp = fiona.open(nodes_strongest_fullpath, mode='w', driver='ESRI Shapefile',
                           schema=node_schema, crs="EPSG:4326")

    for record in nodes_sf.shapeRecords():
        if tuple(record.shape.points[0]) in largest:
            nodeDict = {
                'geometry': {'type': 'Point',
                             'coordinates': tuple(record.shape.points[0])},
                'properties': {'ID': record.record.ID},
            }
            point_shp.write(nodeDict)

    point_shp.close()

