import mysql.connector
from Model.Event import Event


class DataBase:

    def __init__(self):
        # Verbindung zum MariaDB-Server
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="dashboard",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        # Cursor für Datenbankabfrage
        self.cursor = self.connection.cursor(dictionary=True)

    def execute_query(self, query, param=None):
        # Führt eine Abfrage mit optionalen Parametern aus
        self.cursor.execute(query, param)

        # Holt Ergebnisse, wenn die Abfrage eine SELECT-Abfrage ist
        if query.strip().startswith("SELECT"):
            self.cursor.fetchall()

        # Bestätigt die Änderung in der Datenbank
        self.connection.commit()

    def fetch_all(self, query, param=None):
        # Führt eine Abfrage aus und gibt alle Ergebnisse zurück
        self.cursor.execute(query, param)
        return self.cursor.fetchall()

    def fetch_one(self, query, param=None):
        # Führt eine Abfrage aus und gibt das erste Ergebnis zurück
        self.cursor.execute(query, param)
        return self.cursor.fetchone()

    def close(self):
        # Schließt den Cursor und die Datenbankverbindung
        self.cursor.close()
        self.connection.close()

    def save_modul(self, modul, student):
        # Überprüft, ob das Modul bereits in der Datenbank vorhanden ist
        query = "SELECT id FROM Modul WHERE modul_id = %s AND student_id = %s"
        param = (modul.get_modul_id(), student.student_id)
        result = self.fetch_one(query, param)

        if result:
            # Aktualisiert das Modul, wenn es bereits existiert
            modul_id = result["id"]
            query = """UPDATE Modul 
            SET acronym = %s, title = %s, exam_format = %s, image_path = %s, status = %s, 
            start_date = %s, end_date = %s, deadline = %s, exam_date = %s, grade = %s, student_id = %s
            WHERE id = %s"""
            param = (modul.get_acronym(), modul.get_title(), modul.get_exam_format(), modul.image_path,
                     modul.get_status(), modul.get_start_date(), modul.get_end_date(), modul.get_deadline(),
                     modul.get_exam_date(), modul.get_grade(), student.student_id, modul_id)

            try:
                self.execute_query(query, param)

            except Exception as e:
                print(f"Fehler beim Updaten des Moduls: {e}")

        else:
            # Fügt das Modul hinzu, wenn es noch nicht existiert
            query = """INSERT INTO Modul (modul_id, acronym, title, exam_format, image_path, status, start_date, 
            end_date, deadline, exam_date, grade, student_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            param = (modul.get_modul_id(), modul.get_acronym(), modul.get_title(), modul.get_exam_format(),
                     modul.image_path, modul.get_status(), modul.get_start_date(), modul.get_end_date(),
                     modul.get_deadline(), modul.get_exam_date(), modul.get_grade(), student.student_id)

            try:
                self.execute_query(query, param)

            except Exception as e:
                print(f"Fehler beim Erstellen des Moduls: {e}")

    def load_modul(self, modul, student):
        # Lädt ein Modul aus der Datenbank basierend auf Modul- und StudentID
        query = "SELECT * FROM Modul WHERE modul_id = %s AND student_id = %s"
        param = (modul.get_modul_id(), student.student_id)
        result = self.fetch_one(query, param)

        if result:
            # Setzt die Modul-Daten, wenn ein Ergebnis vorliegt
            modul.set_acronym(result["acronym"])
            modul.set_title(result["title"])
            modul.set_exam_format(result["exam_format"])
            modul.image_path = result["image_path"]
            modul.set_status(result["status"])
            modul.start_date = result["start_date"]
            modul.end_Date = result["end_date"]
            modul.deadline = result["deadline"]
            modul.set_exam_date(result["exam_date"])
            modul.set_grade(result["grade"])
            modul.set_modul_id(result["modul_id"])

    def save_event(self, event, student):
        # Überprüft, ob das Event bereits in der Datenbank existiert
        query = "SELECT event_id FROM Events WHERE event_id = %s AND student_id = %s"
        param = (event.event_id, student.student_id)
        result = self.fetch_one(query, param)

        if not result:
            # Fügt das Event hinzu, wenn es noch nicht existiert
            query = """INSERT INTO Events (event_id, title, event_date, is_exam_event, student_id)
            VALUES (%s, %s, %s, %s, %s)"""
            param = (event.event_id, event.event_title, event.event_date, event.is_exam_event, student.student_id)

            try:
                self.execute_query(query, param)

            except Exception as e:
                print(f"Fehler beim speichern des Events: {e}")

    def load_events(self, student):
        # Läde alle Events eines Studenten aus der Datenabnk
        query = "SELECT * FROM Events WHERE student_id = %s"
        param = (student.student_id,)
        results = self.fetch_all(query, param)

        event_list = []

        if results:
            # Erstellt eine Liste von Event-Objekten basierend auf den Ergebnissen
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
            return []

    def get_events(self, student):
        # Lädt die Events des Studenten und speichert sie in der Studenten-Event-Liste
        events = self.load_events(student)

        if events:
            student.event_list = events

        else:
            student.event_list = []

        return events

    def delete_event(self, event_id, student):
        # Findet und löscht ein Event aus der Datenbank
        query = "SELECT id FROM Events WHERE event_id = %s AND student_id = %s"
        param = (event_id, student.student_id)
        result = self.fetch_one(query, param)
        result_id = result["id"]

        query = "DELETE FROM Events WHERE id = %s"
        param = (result_id,)

        try:
            self.execute_query(query, param)
            self.connection.commit()

        except Exception as e:
            print(f"Fehler beim löschen des Events: {e}")

    def save_avg_grade(self, student):
        # Überprüft, ob der Notendurchschnitt bereits existiert und aktualisiert ihn
        query = "SELECT * FROM AvgGrade WHERE student_id = %s"
        param = (student.student_id,)
        result = self.fetch_one(query, param)

        if result:
            # Aktualisiert den Notendurchschnitt, wenn er bereits existiert
            query = """UPDATE AvgGrade
            SET planned_avg_grade = %s, actual_avg_grade = %s, actual_avg_grade_is_better_than_planned = %s
            WHERE student_id = %s"""
            param = (student.avg_grade.planned_avg_grade, student.avg_grade.actual_avg_grade,
                     student.avg_grade.actual_avg_grade_is_better_than_planned, student.student_id)
            self.execute_query(query, param)

        else:
            # Fügt den Notendurchschnitt hinzu, wenn er noch nicht existiert
            query = """INSERT INTO AvgGrade (student_id, planned_avg_grade, actual_avg_grade, 
            actual_avg_grade_is_better_than_planned)
            VALUES (%s, %s, %s, %s)"""
            param = (student.student_id, student.avg_grade.planned_avg_grade, student.avg_grade.actual_avg_grade,
                     student.avg_grade.actual_avg_grade_is_better_than_planned)
            self.execute_query(query, param)

    def load_avg_grade(self, student):
        # Lädt den Notendurchschnitt eines Studenten aus der Datenbank
        query = "SELECT * FROM AvgGrade WHERE student_id = %s"
        param = (student.student_id,)
        result = self.fetch_one(query, param)

        if result:
            # Setzt die Werte des Notendurchschnitts auf das Studentenobjekt
            student.planned_avg_grade = result["planned_avg_grade"]
            student.avg_grade.set_actual_avg_grade(result["actual_avg_grade"])
            student.avg_grade.set_actual_avg_grade_is_better_than_planned(
                result["actual_avg_grade_is_better_than_planned"])

        else:
            print("Kein geplanter Notendurchschnitt in der Datenbank gefunden.")

    def save_student(self, student):
        # Speichert oder aktualisiert den Studenten in der Datenbank
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
            params = (student.planned_avg_grade, student.graduation_date, student.get_expected_graduation_date(),
                      student.get_is_expected_before_graduation(), student.student_id)
            self.execute_query(query, params)

        else:
            query = """
            INSERT INTO Student (student_id, last_name, first_name, number, study_start_date, planned_avg_grade,
            graduation_date, expected_graduation_date, is_expected_before_graduation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (student.student_id, student.last_name, student.first_name, student.number,
                      student.study_start_date, student.planned_avg_grade, student.graduation_date,
                      student.get_expected_graduation_date(), student.get_is_expected_before_graduation())
            self.execute_query(query, params)
            student.student_id = self.cursor.lastrowid
