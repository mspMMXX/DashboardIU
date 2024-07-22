class AvgGrade:

    def __init__(self):
        self.planned_avg_grade = None
        self.actual_avg_grade = None
        self.actual_avg_grade_is_better_than_planned = None

    def calc_avg_grade(self, student_moduls):
        sum_grade = 0.0
        sum_completed_moduls = 0.0
        for modul in student_moduls.values():
            if modul.grade is not None:
                sum_grade += float(modul.grade)
                sum_completed_moduls += 1
        self.actual_avg_grade = sum_grade / sum_completed_moduls if sum_completed_moduls > 0 else None

    def calc_avg_is_better_than_planned(self, planned_avg_grade):
        if self.actual_avg_grade is None or planned_avg_grade is None:
            self.actual_avg_grade_is_better_than_planned = None
        elif self.actual_avg_grade <= planned_avg_grade:
            self.actual_avg_grade_is_better_than_planned = True
        else:
            self.actual_avg_grade_is_better_than_planned = False
