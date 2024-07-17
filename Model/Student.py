from Model.StudyProgram import StudyProgram
from Model.AvgGrade import AvgGrade
from Model.Event import Event
from datetime import datetime as dt, timedelta as td


class Student:

    def __init__(self):
        self.studetn_id = 1
        self.first_name = "Max"
        self.last_name = "Mustermann"
        self.number = "23404383"
        self.study_program = StudyProgram()
        self.study_start_date = dt(2024, 6, 12)
        self.graduation_date = None
        self.expected_graduation_date = None
        self.is_expected_before_graduation = None
        self.planned_avg_grade = None
        self.avg_grade = AvgGrade(self.planned_avg_grade)
        self.event_list = []
        self.modul_list = {}
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
        if self.modul_list == {}:
            self.modul_list = self.study_program.modul_list

    def calc_graduation_date(self):
        try:
            new_year = self.study_start_date.year + self.study_program.study_duration
            self.graduation_date = self.study_start_date.replace(year=new_year)
        except ValueError as e:
            print(f"Fehler beim Berechnen des Abschlussdatums: {e}")
            self.graduation_date = None

    def calc_expected_graduation_date(self):
        sum_modul = 0
        total_days_needed = 0

        for modul in self.modul_list.values():
            if modul.status == "Abgeschlossen":
                total_days_needed += (modul.end_Date - modul.start_date).days
                sum_modul += 1

        if sum_modul != 0:
            days_to_finish = (total_days_needed / sum_modul) * 36
            days = td(days=days_to_finish)

            self.expected_graduation_date = self.study_start_date + days

    def calc_is_expected_before_graduation(self):
        if self.expected_graduation_date is not None and (self.graduation_date >= self.expected_graduation_date):
            self.is_expected_before_graduation = True
        elif self.expected_graduation_date is not None and (self.graduation_date < self.expected_graduation_date):
            self.is_expected_before_graduation = False
        else:
            self.is_expected_before_graduation = False

    def set_planned_avg_grade(self, planned_grade):
        self.planned_avg_grade = planned_grade
