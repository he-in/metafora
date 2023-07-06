import random


class Node:
    def __init__(self, uid, longitude_e=None, latitude_n=None, node_duration_d=None):
        self.uid = uid
        self.longitude_e = longitude_e
        self.latitude_n = latitude_n
        self.node_t_start_d = 0
        self.node_t_finish_d = 0
        self.node_duration_d = node_duration_d

    def node_wait(self):
        self.node_duration_d = random.randrange(self.node_t_start_d, self.node_t_finish_d)


def create_nodesDB():

