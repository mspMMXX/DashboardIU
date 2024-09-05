from Model.StudyProgram import StudyProgram
from Model.AvgGrade import AvgGrade
from Model.Event import Event
from Data.DataBase import DataBase
from datetime import datetime as dt, timedelta as td


class Student:

    def __init__(self):
        self.student_id = 1
        self.first_name = "Max"
        self.last_name = "Mustermann"
        self.number = "23404383"
        self.study_program = StudyProgram()
        self.study_start_date = dt(2024, 6, 12)
        self.graduation_date = None
        self.expected_graduation_date = self.graduation_date
        self.is_expected_before_graduation = None
        self.planned_avg_grade = None
        self.avg_grade = AvgGrade()
        self.modul_list = {}
        self.db = DataBase()
        print("Lade Events für den Studenten")
        self.event_list = self.db.get_events(self)
        print(f"Anzahl der Events nach Abruf: {len(self.event_list)}")
        self.db.save_student(self)
        self.initialize_moduls()
        self.calc_graduation_date()

    def get_number(self):
        return self.number

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_expected_graduation_date(self):
        return self.expected_graduation_date

    def get_graduation_date(self):
        return self.graduation_date

    def get_study_start_date_str(self):
        return self.study_start_date.strftime("%d.%m.%Y")

    def get_planned_avg_grade(self):
        return self.planned_avg_grade

    def get_student_modul_list(self):
        return self.modul_list

    def create_event(self, event_title, event_date):
        try:
            event = Event(event_title, event_date)
            self.db.save_event(event, self)
            self.event_list = self.db.get_events(self)
            print(f"Event-Liste nach dem Erstellen: {self.event_list}")
        except Exception as e:
            print(f"Fehler beim erstellen des Events: {e}")

    def remove_event(self, event_id):
        try:
            self.db.delete_event(event_id, self)
            self.event_list = self.db.get_events(self)
            print(f"Event-Liste nach dem Löschen: {self.event_list}")
        except Exception as e:
            print(f"Fehler beim Löschen des Events: {e}")

    def initialize_moduls(self):
        mod_list = self.study_program.modul_list
        try:
            for modul in mod_list.values():
                self.db.load_modul(modul, self)
                self.db.save_modul(modul, self)
        except Exception as e:
            print(f"Fehler beim laden der Module: {e}")
        self.modul_list = mod_list

    def calc_graduation_date(self):
        try:
            new_year = self.study_start_date.year + self.study_program.study_duration
            self.graduation_date = self.study_start_date.replace(year=new_year)
        except ValueError as e:
            print(f"Fehler beim berechnen des Abschlussdatums: {e}")
            self.graduation_date = None

    def calc_avg_grade(self):
        self.avg_grade.calc_avg_grade(self.modul_list)

    def set_planned_avg_grade(self, planned_grade):
        self.planned_avg_grade = planned_grade
        self.avg_grade.planned_avg_grade = planned_grade

    def calc_expected_graduation_date(self):
        total_days_needed = sum(
            (modul.end_Date - modul.start_date).days for modul in self.modul_list.values()
            if modul.status == "Abgeschlossen" and isinstance(modul.start_date, dt) and isinstance(modul.end_Date, dt)
        )
        sum_modul = sum(
            1 for modul in self.modul_list.values()
            if modul.status == "Abgeschlossen"
        )

        if sum_modul != 0:
            days_to_finish = (total_days_needed / sum_modul) * len(self.modul_list)
            self.expected_graduation_date = self.study_start_date + td(days=days_to_finish)
        else:
            self.expected_graduation_date = self.graduation_date

    def calc_is_expected_before_graduation(self):
        if self.expected_graduation_date is not None and (self.graduation_date >= self.expected_graduation_date):
            self.is_expected_before_graduation = True
        elif self.expected_graduation_date is not None and (self.graduation_date < self.expected_graduation_date):
            self.is_expected_before_graduation = False
        else:
            self.is_expected_before_graduation = False
