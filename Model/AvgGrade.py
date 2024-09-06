class AvgGrade:

    def __init__(self):
        self.actual_avg_grade = None
        self.actual_avg_grade_is_better_than_planned = None

    def get_actual_avg_grade(self):
        # Gibt den aktuellen Notendurchschnitt zurück
        return self.actual_avg_grade

    def set_actual_avg_grade(self, grade):
        # Setzt den aktuellen Notendurchschnitt
        self.actual_avg_grade = grade

    def get_actual_avg_is_better_than_planned(self):
        # Gibt zurück, ob der aktuelle Notendurchschnitt besser als der geplante ist
        if self.actual_avg_grade_is_better_than_planned is None:
            return False
        else:
            return self.actual_avg_grade_is_better_than_planned

    def set_actual_avg_grade_is_better_than_planned(self, is_better):
        # Setzt den Wert, ob der aktuelle Notendurchschnitt besser als der geplante ist
        self.actual_avg_grade_is_better_than_planned = is_better

    def calc_avg_grade(self, student_moduls):
        # Berechnet den aktuellen Notendurchschnitt basierend auf den Noten der abgeschlossenen Module
        sum_grade = 0.0
        sum_completed_moduls = 0.0

        # Iteriert über alle Module des Studenten
        for modul in student_moduls.values():
            # Nur Module mit einer vorhandenen Note werden brücksichtigt
            if modul.get_grade() is not None:
                sum_grade += float(modul.get_grade())
                sum_completed_moduls += 1

                # Berechnet den Notendurchschnitt oder setzt ihn auf None, wenn keine Module abgeschlossen sind
        self.actual_avg_grade = sum_grade / sum_completed_moduls if sum_completed_moduls > 0 else None

    def calc_avg_is_better_than_planned(self, planned_avg_grade):
        # Vergleicht den aktuellen Notendurchschnitt mit dem geplanten Durchschnitt
        if self.actual_avg_grade is None or planned_avg_grade is None:
            # Wenn einer der WErte None ist, kann kein Vergleich gemacht werden
            self.actual_avg_grade_is_better_than_planned = None
        elif self.actual_avg_grade <= planned_avg_grade:
            # Der aktuelle Notendurchschnitt ist besser oder gleich dem geplanten
            self.actual_avg_grade_is_better_than_planned = True
        else:
            # Der aktuelle Notendurchschnitt ist schlechter als der geplante
            self.actual_avg_grade_is_better_than_planned = False
