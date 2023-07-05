# all the imports
import os


# Microdata

# GIS input

network_name = 'Nanjing'
period = 'AM'
day = 'Weekday'
year_month = '2019-10'  # format needs to be YYYY-MM
base_folder_path = '/home/hein/Documents/nanjing_modelling/data/'

# input files
roads_folder = '/home/hein/Documents/nanjing_modelling/data/'
roads_shp = 'gis_osm_roads_free_1.shp'

# output files
Nodes_folder = '/home/he-in/Documents/Nanjing/Xinjiekou_station/'
Nodes_shp = 'Nodes.shp'
Links_folder = '/home/hein/Documents/nanjing_modelling/data/'
Links_shp = 'Links.shp'
Nodes_strongest_folder = '/home/he-in/Documents/Nanjing/Xinjiekou_station/'
Nodes_strongest_shp = 'Nodes_strongest.shp'
Links_strongest_folder = '/home/he-in/Documents/Nanjing/Xinjiekou_station/'
Links_strongest_shp = 'Links_strongest.shp'


# functions to run
create_simplified_from_road = True
create_nodes_from_roads = False
create_links_from_roads = False
create_network_strongest_nj = False

if create_simplified_from_road:
    roads_fullpath = roads_folder + roads_shp
    links_fullpath = Links_folder + Links_shp
    gen_simple_from_roads(roads_fullpath, links_fullpath)

if create_nodes_from_roads:
    roads_fullpath = roads_folder + roads_shp
    nodes_fullpath = Nodes_folder + Nodes_shp
    nodes_list = gen_nodes_from_roads(roads_fullpath, nodes_fullpath)

if create_links_from_roads:
    nodes_fullpath = Nodes_folder + Nodes_shp
    roads_fullpath = roads_folder + roads_shp
    links_fullpath = Links_folder + Links_shp
    if not create_nodes_from_roads:
        nodes_list = []
    gen_links_from_roads(nodes_fullpath, roads_fullpath, links_fullpath, nodes_list)

if create_network_strongest_nj:
    nodes_fullpath = Nodes_folder + Nodes_shp
    links_fullpath = Links_folder + Links_shp
    nodes_strongest_fullpath = Nodes_strongest_folder + Nodes_strongest_shp
    links_strongest_fullpath = Links_strongest_folder + Links_strongest_shp
    network = gen_strongest_network(nodes_fullpath, links_fullpath, nodes_strongest_fullpath, links_strongest_fullpath)
