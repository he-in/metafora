class LinkHelper:
    def __init__(self, uid, link_id=None, max_ppl=None, plus_info_links=None, plus_agency=None, plus_mobility=None,
                 minus_finance=None):
        self.uid = uid
        self.link_id = link_id   # Link ID
        # self.origin = Link.a_node
        self.max_ppl = max_ppl  # The number of people the helper can help at one time
        self.plus_info_links = plus_info_links # Link information
        self.plus_agency = plus_agency
        self.plus_mobility = plus_mobility
        self.minus_finance = minus_finance
        self.helping = False  # Midst helping
        self.history_help = 0

    def move(self):
        if not self.travelling:
            self.travelling = True