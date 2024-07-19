from datetime import datetime, timedelta


class Modul:

    def __init__(self, modul_id, acronym, title, exam_format, image_path):
        self.modul_id = modul_id
        self.acronym = acronym
        self.title = title
        self.status = "Offen"
        self.exam_format = exam_format
        self.start_date = None
        self.end_Date = None
        self.deadline = None
        self.exam_date = None
        self.grade = None
        self.image_path = image_path

    def set_status(self, status):
        self.status = status

    def set_start_date(self):
        if self.status == "In Bearbeitung":
            self.start_date = datetime.now()

    def set_end_date(self):
        if self.status == "Abgeschlossen":
            if self.end_Date is None:
                self.end_Date = datetime.now()

    def set_deadline(self):
        time_for_modul = 4 * 365 / 36
        if self.start_date:
            self.deadline = self.start_date + timedelta(days=time_for_modul)
        else:
            self.deadline = None

    def set_grade(self, grade):
        self.grade = grade

    def update_modul(self, student, status="Offen", start_date=None, exam_date=None, grade=None):
        self.status = status
        self.start_date = start_date
        self.grade = grade
        self.set_exam_date_create_event(student, exam_date)

    def set_exam_date_create_event(self, student, exam_date):
        if isinstance(exam_date, str):
            try:
                exam_date_obj = datetime.strptime(exam_date, "%d.%m.%Y %H:%M")
                self.exam_date = exam_date_obj
            except ValueError as e:
                print(f"Fehler beim Umwandeln des Prüfungstermins: {e}")
                return
        elif isinstance(exam_date, datetime):
            self.exam_date = exam_date
        else:
            print("exam_date muss ein String oder ein datetime-Objekt sein")
            return

        try:
            student.create_event(self.title, self.exam_date)
        except Exception as e:
            print(f"Fehler beim Setzen des Prüfungstermins und Termins: {e}")
