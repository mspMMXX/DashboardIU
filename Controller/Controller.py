from Model.AvgGrade import AvgGrade
from Model.StudyProgram import StudyProgram
from Model.IuInformation import IUInformation


class Controller:

    def __init__(self, student):
        self.student = student
        self.avg_grade = AvgGrade()
        self.study_program = StudyProgram()
        self.iu_information = IUInformation()

    def get_events(self):
        return self.student.event_list

    def get_student_moduls(self):
        return self.student.modul_list

    def update_modul(self, modul_id, status, start_date, exam_date, grade):
        try:
            if modul_id not in self.student.modul_list:
                raise KeyError(f"Modul-ID existiert nicht: {modul_id}")
            modul = self.student.modul_list[modul_id]
            modul.update_modul(self.student, status, start_date.strftime("%d.%m.%Y %H:%M"),
                               exam_date.strftime("%d.%m.%Y %H:%M"), grade)
        except Exception as e:
            print(f"Fehler beim updaten des Moduls ({modul_id}): {e}")

    def create_event(self, title, date):
        try:
            self.student.create_event(title, date)
        except Exception as e:
            print(f"Fehler beim erstellen des Events: {e}")

    def remove_event(self, event_id):
        try:
            self.student.remove_event(event_id)
        except Exception as e:
            print(f"Fehler beim löschen des Events: {e}")

    def calc_avg_grade(self):
        self.student.avg_grade.calc_avg_grade(self.student.modul_list)

    def calc_avg_is_better_than_planned(self):
        self.student.avg_grade.calc_avg_is_better_than_planned()

    def get_avg_is_better_than_planned(self):
        return self.student.avg_grade.actual_avg_grade_is_better_than_planned

    def set_planned_avg_grade(self, planned_avg_grade):
        self.student.avg_grade.planned_avg_grade = planned_avg_grade

    def get_planned_avg_grade(self):
        return self.student.avg_grade.planned_avg_grade

    def calc_expected_graduation_date(self):
        self.student.calc_expected_graduation_date()

    def get_expected_graduation_date(self):
        print(f"Controller: {self.student.expected_graduation_date}")
        return self.student.expected_graduation_date
