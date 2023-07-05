class NodeHelper:
    def __init__(self, uid, location, plus_aspiration=None, plus_agency=None, plus_mobility=None, minus_finance=None,
                 plus_info_transit=None):
        self.uid = uid
        self.location = location  # NodeID
        self.plus_info_transit = plus_info_transit
        self.plus_agency = plus_agency
        self.plus_mobility = plus_mobility
        self.minus_finance = minus_finance
        self.helping = False

    def move(self):
        if not self.travelling:
            self.travelling = True

