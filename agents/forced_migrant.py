import random


class Migrant:
    def __init__(self, uid, size, node_location=None, link_location=None, destination=None, financial_capital=None, aspiration=None,
                 risk_perception=None, agency=None, mobility=None, capability=None, positive_liberty=None,
                 physical_ability=None, mental_energy=None, luck=None,
                 passed_nodes=None, info_links=None, info_transit=None, origin=None):
        self.uid = uid
        self.size = size
        self.node_location = node_location
        self.link_location = None
        self.origin = origin
        self.destination = destination
        self.departure_date = 0
        self.travelling = False
        self.resources = financial_capital
        self.financial_capital = financial_capital
        self.behavioural_properties = aspiration + risk_perception + agency + mobility + capability \
                                      + positive_liberty + physical_ability + mental_energy + luck
        self.aspiration = aspiration
        self.risk_perception = risk_perception
        self.agency = agency
        self.mobility = mobility
        self.capability = capability
        self.positive_liberty = positive_liberty
        self.physical_ability = physical_ability
        self.mental_energy = mental_energy
        self.luck = luck
        self.state = 'IDP'  # 'pas': propspective_asylum_seeker, 'as': asylum_seeker, 'aftp': admitted_for_temp_protection, 'refugee'
        # self.information = information
        self.info_links = info_links # array of binary classification of knowing if a link exists
        self.info_transit = info_transit   # array of binary classification of knowing if a link exists
        self.info_dest = 1  # Have info about destination
        self.passed_nodes = passed_nodes  # Array of nodes
        self.settled = False
        self.leaving_fleeing = 'fleeing'  # 'leaving', 'fleeing'
        self.dest_plan = 'since_beg'  # 'since_beg', 'throughout', 'none'
        self.plan = 'long_term'  # 'long_term', 'aspirations_only', 'short_term', 'none'
        self.routing = 'key_transit'  # 'key_transit', 'optimisation', 'next_stop_only', 'random_routing'

    def plan(self):
        if self.leaving_fleeing == 'leaving':
            self.dest_plan = 'since_beg'
            self.routing = 'key_transit'
        elif self.leaving_fleeing == 'fleeing':
            random_e = 0.3
            random_f = 0.6
            if random.random() < random_e:
                self.dest_plan = 'since_beg'
                self.routing = 'optimisation'
            elif random.random() < random_f:
                self.dest_plan = 'throughout'
                self.routing = 'next_stop_only'
            else:
                self.dest_plan = 'none'
                self.routing = 'random-routing'


class MigrantKPIs:
    def move(self):
        if not self.travelling:
            self.travelling = True

    def stop(self):
        if self.travelling:
            self.travelling = False

    def settle(self):
        self.settled = True



class TransportMode:
    def __init__(self):
        self.mode_name = mode_name  # item from list [walk, bus, truck, train, ferry]
        self.average_speed = average_speed
        self.max_distance = max_distance
        self.max_group_size = max_group_size


class Origin:
    def __init__(self):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


class Destination:
    def __init__(self):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


class Location:
    def __init__(self):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
