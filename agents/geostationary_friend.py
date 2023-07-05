class GeoFriend:
    def __init__(self, uid, location, plus_aspiration=None, plus_agency=None, plus_mobility=None, plus_finance=None):
        self.uid = uid
        self.location = location
        self.plus_aspiration = plus_aspiration
        self.plus_agency = plus_agency
        self.plus_mobility = plus_mobility
        self.plus_finance = plus_finance
        self.helping = False

    def move(self):
        if not self.travelling:
            self.travelling = True