from Model.AvgGrade import AvgGrade
from Model.StudyProgram import StudyProgram
from Model.IuInformation import IUInformation
from Data.DataBase import DataBase
from Model.Event import Event


class Controller:

    def __init__(self, student):
        self.student = student
        self.avg_grade = AvgGrade()
        self.study_program = StudyProgram()
        self.iu_information = IUInformation()
        self.db = DataBase("127.0.0.1", "root", "root", "dashboard", "utf8mb4", "utf8mb4_general_ci")

    def get_events(self):
        events = self.load_events()
        if events is not None:
            self.student.event_list = events
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
            self.save_modul(modul)
        except Exception as e:
            print(f"Fehler beim Updaten des Moduls ({modul_id}): {e}")

    def create_event(self, title, date):
        try:
            self.student.create_event(title, date)
        except Exception as e:
            print(f"Fehler beim Erstellen des Events: {e}")

    def remove_event(self, event_id):
        try:
            self.student.remove_event(event_id)
            self.delete_event(event_id)
        except Exception as e:
            print(f"Fehler beim Löschen des Events: {e}")

    def calc_avg_grade(self):
        self.student.avg_grade.calc_avg_grade(self.student.modul_list)

    def calc_avg_is_better_than_planned(self):
        self.student.avg_grade.calc_avg_is_better_than_planned(self.student.avg_grade.planned_avg_grade)

    def get_avg_is_better_than_planned(self):
        return self.student.avg_grade.actual_avg_grade_is_better_than_planned

    def set_planned_avg_grade(self, planned_avg_grade):
        self.student.set_planned_avg_grade(planned_avg_grade)

    def get_planned_avg_grade(self):
        return self.student.avg_grade.planned_avg_grade

    def calc_expected_graduation_date(self):
        self.student.calc_expected_graduation_date()

    def get_expected_graduation_date(self):
        return self.student.expected_graduation_date

    # DATABASE
    def save_student(self, student):
        query = "SELECT student_id FROM Student WHERE number = %s"
        params = (student.number,)
        result = self.db.fetch_one(query, params)

        if result:
            student.student_id = result["student_id"]
            query = """
            UPDATE Student
            SET planned_avg_grade = %s, graduation_date = %s, expected_graduation_date = %s, 
            is_expected_before_graduation = %s
            WHERE student_id = %s
            """
            params = (student.planned_avg_grade, student.graduation_date, student.expected_graduation_date,
                      student.is_expected_before_graduation, student.student_id)
            self.db.execute_query(query, params)
        else:
            query = """
            INSERT INTO Student (student_id, last_name, first_name, number, study_start_date, planned_avg_grade,
            graduation_date, expected_graduation_date, is_expected_before_graduation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (student.student_id, student.last_name, student.first_name, student.number,
                      student.study_start_date, student.planned_avg_grade, student.graduation_date,
                      student.expected_graduation_date, student.is_expected_before_graduation)
            self.db.execute_query(query, params)
            student.student_id = self.db.cursor.lastrowid

    def save_modul(self, modul):
        query = "SELECT id FROM Modul WHERE modul_id = %s AND student_id = %s"
        param = (modul.modul_id, self.student.student_id)
        result = self.db.fetch_one(query, param)

        if result:
            modul_id = result["id"]
            query = """UPDATE Modul 
            SET acronym = %s, title = %s, exam_format = %s, image_path = %s, status = %s, 
            start_date = %s, end_date = %s, deadline = %s, exam_date = %s, grade = %s, student_id = %s
            WHERE id = %s"""
            param = (modul.acronym, modul.title, modul.exam_format, modul.image_path, modul.status, modul.start_date,
                     modul.end_Date, modul.deadline, modul.exam_date, modul.grade, self.student.student_id,
                     modul_id)

            try:
                self.db.execute_query(query, param)
            except Exception as e:
                print(f"Fehler beim Updaten des Moduls: {e}")
        else:
            query = """INSERT INTO Modul (modul_id, acronym, title, exam_format, image_path, status, start_date, 
            end_date, deadline, exam_date, grade, student_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            param = (modul.modul_id, modul.acronym, modul.title, modul.exam_format, modul.image_path, modul.status,
                     modul.start_date, modul.end_Date, modul.deadline, modul.exam_date, modul.grade,
                     self.student.student_id)

            try:
                self.db.execute_query(query, param)
            except Exception as e:
                print(f"Fehler beim Erstellen des Moduls: {e}")

    def load_modul(self, modul):
        print("Laden der Module")
        query = "SELECT * FROM Modul WHERE modul_id = %s AND student_id = %s"
        param = (modul.modul_id, self.student.student_id)
        result = self.db.fetch_one(query, param)

        if result:
            modul.acronym = result["acronym"]
            modul.title = result["title"]
            modul.exam_format = result["exam_format"]
            modul.image_path = result["image_path"]
            modul.status = result["status"]
            modul.start_date = result["start_date"]
            modul.end_Date = result["end_date"]
            modul.deadline = result["deadline"]
            modul.exam_date = result["exam_date"]
            modul.grade = result["grade"]
            modul.modul_id = result["modul_id"]
            print(f"Modul geladen: {modul}")

    def save_event(self, event):
        query = "SELECT event_id FROM Events WHERE event_id = %s AND student_id = %s"
        param = (event.event_id, self.student.student_id)
        result = self.db.fetch_one(query, param)

        if not result:
            query = """INSERT INTO Events (event_id, title, event_date, is_exam_event, student_id)
            VALUES (%s, %s, %s, %s, %s)"""
            param = (event.event_id, event.event_title, event.event_date, event.is_exam_event, self.student.student_id)

            try:
                self.db.execute_query(query, param)
            except Exception as e:
                print(f"Fehler beim speichern des Events: {e}")

    def load_events(self):
        query = "SELECT * FROM Events WHERE student_id = %s"
        param = (self.student.student_id,)
        results = self.db.fetch_all(query, param)

        event_list = []

        if results:
            for event in results:
                event_id = event["event_id"]
                event_title = event["title"]
                event_date = event["event_date"]
                is_exam_event = event["is_exam_event"]

                event = Event(event_title, event_date, is_exam_event)
                event.event_id = event_id
                event_list.append(event)
            return event_list
        else:
            return None

    def delete_event(self, event_id):
        query = "SELECT id FROM Events WHERE event_id = %s AND student_id = %s"
        param = (event_id, self.student.student_id)
        result = self.db.fetch_one(query, param)
        result_id = result["id"]

        query = "DELETE FROM Events WHERE id = %s"
        param = (result_id,)
        try:
            self.db.execute_query(query, param)
        except Exception as e:
            print(f"Fehler beim löschen des Events: {e}")

    def save_avg_grade(self, student):
        query = "SELECT * FROM AvgGrade WHERE student_id = %s"
        param = (student.student_id,)
        result = self.db.fetch_one(query, param)

        if result:
            query = """UPDATE AvgGrade
            SET planned_avg_grade = %s, actual_avg_grade = %s, actual_avg_grade_is_better_than_planned = %s
            WHERE student_id = %s"""
            param = (student.avg_grade.planned_avg_grade, student.avg_grade.actual_avg_grade,
                     student.avg_grade.actual_avg_grade_is_better_than_planned, student.student_id)
            self.db.execute_query(query, param)
        else:
            query = """INSERT INTO AvgGrade (student_id, planned_avg_grade, actual_avg_grade, 
            actual_avg_grade_is_better_than_planned)
            VALUES (%s, %s, %s, %s)"""
            param = (student.student_id, student.avg_grade.planned_avg_grade, student.avg_grade.actual_avg_grade,
                     student.avg_grade.actual_avg_grade_is_better_than_planned)
            self.db.execute_query(query, param)

    def load_avg_grade(self, student):
        query = "SELECT * FROM AvgGrade WHERE student_id = %s"
        param = (student.student_id,)
        result = self.db.fetch_one(query, param)

        if result:
            student.avg_grade.planned_avg_grade = result["planned_avg_grade"]
            student.avg_grade.actual_avg_grade = result["actual_avg_grade"]
            student.avg_grade.actual_avg_grade_is_better_than_planned = (
                result)["actual_avg_grade_is_better_than_planned"]

    def cleanup(self):
        self.db.close()
