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

    def get_modul_id(self):
        return self.modul_id

    def set_modul_id(self, modul_id):
        self.modul_id = modul_id

    def get_acronym(self):
        return self.acronym

    def set_acronym(self, acronym):
        self.acronym = acronym

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_exam_format(self):
        return self.exam_format

    def set_exam_format(self, exam_format):
        self.exam_format = exam_format

    def get_start_date(self):
        return self.start_date

    def set_start_date(self):
        if self.status == "In Bearbeitung":
            self.start_date = datetime.now()

    def get_end_date(self):
        return self.end_Date

    def set_end_date(self):
        if self.status == "Abgeschlossen":
            if self.end_Date is None:
                self.end_Date = datetime.now()

    def get_deadline(self):
        return self.deadline

    def set_deadline(self):
        time_for_modul = 4 * 365 / 36
        if self.start_date:
            self.deadline = self.start_date + timedelta(days=time_for_modul)
        else:
            self.deadline = None

    def get_exam_date(self):
        return self.exam_date

    def set_exam_date(self, exam_date):
        self.exam_date = exam_date

    def get_grade(self):
        return self.grade

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
            return

        try:
            student.create_event(self.title, self.exam_date)
        except Exception as e:
            print(f"Fehler beim Setzen des Prüfungstermins und Termins: {e}")
