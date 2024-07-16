from Model.Event import Event


class ExamEvent(Event):

    def __init__(self, event_title, event_date, exam_event_color=None):
        super().__init__(event_title, event_date)
        if exam_event_color is None:
            self.exam_event_color = "red"
        else:
            self.exam_event_color = exam_event_color
