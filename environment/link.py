class Link:
    def __init__(self, uid, a_node=None, b_node=None):
        self.uid = uid
        self.a_node = a_node
        self.b_node = b_node
        self.direction = None
        self.link_length = link_length
        self.link_t_start_d = 0
        self.link_speed = 20  # km/day
        self.link_t_finish_d = link_length/self.link_speed #  deafult = 20 km/day
        self.link_duration_d = link_duration_d


def create_linksDB():


