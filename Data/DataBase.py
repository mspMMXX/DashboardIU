import mysql.connector
from Model.Event import Event


class DataBase:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="dashboard",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        self.cursor = self.connection.cursor(
            dictionary=True)

    def execute_query(self, query, param=None):
        self.cursor.execute(query, param)
        if query.strip().startswith("SELECT"):
            self.cursor.fetchall()
        self.connection.commit()

    def fetch_all(self, query, param=None):
        self.cursor.execute(query, param)
        return self.cursor.fetchall()

    def fetch_one(self, query, param=None):
        self.cursor.execute(query, param)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def load_avg_grade(self, student):
        query = "SELECT * FROM AvgGrade WHERE student_id = %s"
        param = (student.student_id,)
        result = self.fetch_one(query, param)

        if result:
            student.planned_avg_grade = result["planned_avg_grade"]
            student.avg_grade.actual_avg_grade = result["actual_avg_grade"]
            student.avg_grade.actual_avg_grade_is_better_than_planned = (
                result)["actual_avg_grade_is_better_than_planned"]
            print(f"Geplanter Notendurchschnitt geladen: {student.planned_avg_grade}")
        else:
            print("Kein geplanter Notendurchschnitt in der Datenbank gefunden.")

    def save_modul(self, modul, student):
        query = "SELECT id FROM Modul WHERE modul_id = %s AND student_id = %s"
        param = (modul.modul_id, student.student_id)
        result = self.fetch_one(query, param)

        if result:
            modul_id = result["id"]
            query = """UPDATE Modul 
            SET acronym = %s, title = %s, exam_format = %s, image_path = %s, status = %s, 
            start_date = %s, end_date = %s, deadline = %s, exam_date = %s, grade = %s, student_id = %s
            WHERE id = %s"""
            param = (modul.acronym, modul.title, modul.exam_format, modul.image_path, modul.status, modul.start_date,
                     modul.end_Date, modul.deadline, modul.exam_date, modul.grade, student.student_id,
                     modul_id)

            try:
                self.execute_query(query, param)
            except Exception as e:
                print(f"Fehler beim Updaten des Moduls: {e}")
        else:
            query = """INSERT INTO Modul (modul_id, acronym, title, exam_format, image_path, status, start_date, 
            end_date, deadline, exam_date, grade, student_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            param = (modul.modul_id, modul.acronym, modul.title, modul.exam_format, modul.image_path, modul.status,
                     modul.start_date, modul.end_Date, modul.deadline, modul.exam_date, modul.grade,
                     student.student_id)

            try:
                self.execute_query(query, param)
            except Exception as e:
                print(f"Fehler beim Erstellen des Moduls: {e}")

    def load_modul(self, modul, student):
        print("Laden der Module")
        query = "SELECT * FROM Modul WHERE modul_id = %s AND student_id = %s"
        param = (modul.modul_id, student.student_id)
        result = self.fetch_one(query, param)

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

    def get_events(self, student):
        print(f"Student-ID beim Abrufen der Events: {student.student_id}")
        events = self.load_events(student)
        if events:
            student.event_list = events
            print(f"Event-Liste nach dem Laden: {student.event_list}")
        else:
            student.event_list = []
        print(f"Anzahl der Events, die aus der Datenbank geladen wurden (get_events): {len(events)}")
        return events

    def save_event(self, event, student):
        query = "SELECT event_id FROM Events WHERE event_id = %s AND student_id = %s"
        param = (event.event_id, student.student_id)
        result = self.fetch_one(query, param)

        if not result:
            query = """INSERT INTO Events (event_id, title, event_date, is_exam_event, student_id)
            VALUES (%s, %s, %s, %s, %s)"""
            param = (event.event_id, event.event_title, event.event_date, event.is_exam_event, student.student_id)

            try:
                self.execute_query(query, param)
            except Exception as e:
                print(f"Fehler beim speichern des Events: {e}")

    def load_events(self, student):
        print("Wird ausgelöst: load_events")
        query = "SELECT * FROM Events WHERE student_id = %s"
        param = (student.student_id,)
        print(f"SQL-Abfrage: {query} mit Parametern: {param}")
        results = self.fetch_all(query, param)
        print(f"Ergebnisse der SQL-Abfrage: {results}")

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

            print(
                f"Anzahl der Events, die aus der Datenbank geladen wurden (load_events): {len(results)}")
            return event_list
        else:
            print("Keine Events in der Datenbank gefunden")  # Debug-Ausgabe
            return []

    def delete_event(self, event_id, student):
        query = "SELECT id FROM Events WHERE event_id = %s AND student_id = %s"
        param = (event_id, student.student_id)
        result = self.fetch_one(query, param)
        result_id = result["id"]

        query = "DELETE FROM Events WHERE id = %s"
        param = (result_id,)
        try:
            self.execute_query(query, param)
            self.connection.commit()
            print(f"Event erfolgreich gelöscht: {event_id}")
        except Exception as e:
            print(f"Fehler beim löschen des Events: {e}")

    def save_avg_grade(self, student):
        query = "SELECT * FROM AvgGrade WHERE student_id = %s"
        param = (student.student_id,)
        result = self.fetch_one(query, param)

        if result:
            query = """UPDATE AvgGrade
            SET planned_avg_grade = %s, actual_avg_grade = %s, actual_avg_grade_is_better_than_planned = %s
            WHERE student_id = %s"""
            param = (student.avg_grade.planned_avg_grade, student.avg_grade.actual_avg_grade,
                     student.avg_grade.actual_avg_grade_is_better_than_planned, student.student_id)
            self.execute_query(query, param)
        else:
            query = """INSERT INTO AvgGrade (student_id, planned_avg_grade, actual_avg_grade, 
            actual_avg_grade_is_better_than_planned)
            VALUES (%s, %s, %s, %s)"""
            param = (student.student_id, student.avg_grade.planned_avg_grade, student.avg_grade.actual_avg_grade,
                     student.avg_grade.actual_avg_grade_is_better_than_planned)
            self.execute_query(query, param)

    def save_student(self, student):
        query = "SELECT student_id FROM Student WHERE number = %s"
        params = (student.number,)
        result = self.fetch_one(query, params)

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
            self.execute_query(query, params)
        else:
            query = """
            INSERT INTO Student (student_id, last_name, first_name, number, study_start_date, planned_avg_grade,
            graduation_date, expected_graduation_date, is_expected_before_graduation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (student.student_id, student.last_name, student.first_name, student.number,
                      student.study_start_date, student.planned_avg_grade, student.graduation_date,
                      student.expected_graduation_date, student.is_expected_before_graduation)
            self.execute_query(query, params)
            student.student_id = self.cursor.lastrowid
