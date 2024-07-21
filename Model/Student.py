from Model.StudyProgram import StudyProgram
from Model.AvgGrade import AvgGrade
from Model.Event import Event
from datetime import datetime as dt, timedelta as td
from Controller.Controller import Controller


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
        self.event_list = []
        self.modul_list = {}
        self.controller = Controller(self)
        self.controller.save_student(self)
        self.initialize_moduls()
        self.calc_graduation_date()

    def create_event(self, event_title, event_date):
        event = Event(event_title, event_date)
        self.event_list.append(event)

    def remove_event(self, event_id):
        for event in self.event_list:
            if event_id == event.event_id:
                self.event_list.remove(event)

    def initialize_moduls(self):
        mod_list = self.study_program.modul_list
        try:
            for modul in mod_list.values():
                self.controller.load_modul(modul)
                self.controller.save_modul(modul)
        except Exception as e:
            print(f"Fehler beim laden der Module: {e}")
        self.modul_list = mod_list

    def calc_graduation_date(self):
        try:
            new_year = self.study_start_date.year + self.study_program.study_duration
            self.graduation_date = self.study_start_date.replace(year=new_year)
        except ValueError as e:
            print(f"Fehler beim Berechnen des Abschlussdatums: {e}")
            self.graduation_date = None

    def set_planned_avg_grade(self, planned_grade):
        self.planned_avg_grade = planned_grade

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
            days_to_finish = (total_days_needed / sum_modul) * 36
            self.expected_graduation_date = self.study_start_date + td(days=days_to_finish)
        else:
            self.expected_graduation_date = self.graduation_date

        print(f"Student ex_graduation_date: {self.expected_graduation_date}")

    def calc_is_expected_before_graduation(self):
        if self.expected_graduation_date is not None and (self.graduation_date >= self.expected_graduation_date):
            self.is_expected_before_graduation = True
        elif self.expected_graduation_date is not None and (self.graduation_date < self.expected_graduation_date):
            self.is_expected_before_graduation = False
        else:
            self.is_expected_before_graduation = False
