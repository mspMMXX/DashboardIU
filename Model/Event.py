import uuid


class Event:

    def __init__(self, event_title, event_date):
        self.event_id = uuid.uuid4()
        self.event_title = event_title
        self.event_date = event_date
