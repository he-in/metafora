class Network:
    def __init__(self, uid, a_node=None, b_node=None):
        self.nodes_list = nodes_list  # list
        self.nodesDB = nodesDB  # dictionary {ID:longitude, latitude, links from it
        self.neighbor_nodes = neighbor_nodes  # dictionary
        self.links_from_nodes = links_from_nodes  # dictionary
        self.links_list = links_list  # list
        self.linksDB = linksDB  # dictionary {ID:ANode, latitude, links from it
        self.route_links = route_links
        # self.graph = self.graph  # dictionary {Node_ID: {Node2_ID: Link12_ID}, {Node3_ID: Link13_ID}, Node2_ID: {
        # undirected, this means I need to repeat, using an adjacency list


    def create_network(self, nodesDB, linksDB):
        for each n of nodes

