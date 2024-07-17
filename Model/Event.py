import uuid
from datetime import datetime

class Event:

    def __init__(self, event_title, event_date, is_exam_event=False):
        self.event_id = uuid.uuid4()
        self.event_title = event_title
        self.event_date = event_date
        if isinstance(event_date, datetime):
            self.event_date = event_date
        else:
            raise ValueError("event_date must be a datetime object")
        self.is_exam_event = is_exam_event
