import uuid
from datetime import datetime


class Event:

    def __init__(self, event_title, event_date, is_exam_event=False):
        self.event_id = str(uuid.uuid4())
        self.event_title = event_title
        self.event_date = event_date

        # Überprüft, ob das Datum ein datetime-Objekt ist und setzt das Datum des Events
        if isinstance(event_date, datetime):
            self.event_date = event_date

        else:
            # Wenn event_date kein datetime-Objekt ist, wird ein Fehler geworfen
            raise ValueError("event_date must be a datetime object")

        # Setzt, ob das Event eine Prüfung ist (Standardwert: False)
        self.is_exam_event = is_exam_event
