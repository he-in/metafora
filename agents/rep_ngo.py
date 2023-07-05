class NGORep:
    def __init__(self, uid, location=None, total_finance=None, plus_aspiration=None, plus_agency=None,
                 plus_mobility=None, plus_finance=None):
        self.uid = uid
        self.location = location  # Node ID
        self.total_finance = total_finance
        self.plus_aspiration = plus_aspiration
        self.plus_agency = plus_agency
        self.plus_mobility = plus_mobility
        self.plus_finance = plus_finance
        self.organisation = 'UNHCR'  # 'UNHCR', 'NGO', 'IOM'
        self.no_agent_helped = 0

    def move(self):
        if not self.travelling:
            self.travelling = True
