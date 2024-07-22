from Controller.Controller import Controller
from ViewElement.ModulElement import ModulElement
from ViewElement.EventElement import EventElement
from Model.Student import Student
from datetime import datetime
from Model.Modul import Modul
from tkinter import font
import tkinter as tk


class DashboardView:

    def __init__(self):
        self.student = Student()
        self.controller = Controller(self.student)
        self.root = tk.Tk()
        self.root.title("IU Dashboard")
        self.root.geometry("1500x800")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Frames (links, mitte, rechts)
        self.left_frame = tk.Frame(self.root, width=496.6)
        self.left_frame.pack(side="left", fill="y")
        self.center_frame = tk.Frame(self.root, width=496.6)
        self.center_frame.pack(side="left", fill="y")
        self.right_frame = tk.Frame(self.root, width=496.6)
        self.right_frame.pack(side="left", fill="y")

        # Left-Frame Scrollbar Module
        self.canvas = tk.Canvas(self.left_frame, width=496.6)
        scrollbar = tk.Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, width=496.6)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.modules = self.controller.get_student_moduls()
        self.module_index = 0
        self.create_module_elements()

        # Center-Frame
        self.event_title_label = tk.Label(self.center_frame, text="Terminname:")
        self.event_entry = tk.Entry(self.center_frame)
        self.event_title_label.grid(row=0, column=0)
        self.event_entry.grid(row=0, column=1)

        self.event_date_label = tk.Label(self.center_frame, text="Datum:")
        self.event_date_entry = tk.Entry(self.center_frame)
        self.event_date_label.grid(row=0, column=2)
        self.event_date_entry.grid(row=0, column=3)

        self.add_event_button = tk.Button(self.center_frame, text="Neu", command=self.create_new_event)
        self.add_event_button.grid(row=0, column=4)
        self.canvas_c = tk.Canvas(self.center_frame, width=496.6)
        self.scrollbar_c = tk.Scrollbar(self.center_frame, orient="vertical", command=self.canvas_c.yview)
        self.scrollable_frame_c = tk.Frame(self.canvas_c, width=496.6)

        self.scrollable_frame_c.bind(
            "<Configure>",
            lambda e: self.canvas_c.configure(
                scrollregion=self.canvas_c.bbox("all")
            )
        )

        self.canvas_c.create_window((0, 0), window=self.scrollable_frame_c, anchor="nw")
        self.canvas_c.configure(yscrollcommand=self.scrollbar_c.set)

        self.canvas_c.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.scrollbar_c.grid(row=1, column=5, sticky="ns")

        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=1)

        self.schedule_index = 0
        self.create_event_elements()

        # Right-Frame: Übersicht
        # Notendurchschnitt
        self.title_font = font.Font(size=14, weight="bold")

        self.controller.load_avg_grade(self.controller.student)
        self.avg_grade_title = tk.Label(self.right_frame, text="Notendurchschnitt", pady=15, font=self.title_font)
        self.avg_grade_title.grid(row=0, column=1, sticky="e")

        self.planned_grade_label = tk.Label(self.right_frame, text="Geplant:")
        self.planned_grade_entry = tk.Entry(self.right_frame)
        self.actual_avg_grade = self.controller.get_planned_avg_grade()
        self.planned_avg_grade = self.controller.get_planned_avg_grade()
        self.formatted_avg_grade = f"{self.actual_avg_grade: .1f}" if self.actual_avg_grade is not None else "Unbekannt"
        self.planned_grade_entry.insert(0, str(self.planned_avg_grade))
        self.actual_grade_label = tk.Label(self.right_frame, text="Momentan:")
        self.actual_grade_lbl = tk.Label(self.right_frame, text=self.formatted_avg_grade)

        self.planned_grade_label.grid(row=1, column=0, sticky="w")
        self.planned_grade_entry.grid(row=1, column=1, sticky="e")
        self.actual_grade_label.grid(row=2, column=0, sticky="w")
        self.actual_grade_lbl.grid(row=2, column=1, sticky="e")

        self.update_avg_grade_label()
        self.grade_label_color()

        # Studium
        self.study_label = tk.Label(self.right_frame, text="Studium", pady=15, font=self.title_font)
        self.study_label.grid(row=3, column=1, sticky="e")

        self.study_name_label = tk.Label(self.right_frame, text="Studiengang:")
        self.study_name_lbl = tk.Label(self.right_frame, text=self.controller.study_program.course_of_study)
        self.study_name_label.grid(row=4, column=0, sticky="w")
        self.study_name_lbl.grid(row=4, column=1, sticky="e")

        self.study_duration_label = tk.Label(self.right_frame, text="Studiendauer")
        self.study_duration_lbl = tk.Label(self.right_frame, text=self.controller.study_program.study_duration)
        self.study_duration_label.grid(row=5, column=0, sticky="w")
        self.study_duration_lbl.grid(row=5, column=1, sticky="e")

        self.start_label = tk.Label(self.right_frame, text="Studienbeginn:")
        self.start_lbl = tk.Label(self.right_frame, text=self.controller.student.study_start_date.strftime("%d.%m.%Y"))
        self.start_label.grid(row=6, column=0, sticky="w")
        self.start_lbl.grid(row=6, column=1, sticky="e")
        self.end_label = tk.Label(self.right_frame, text="Abschluss:")
        graduation_date = self.controller.student.graduation_date
        self.controller.calc_expected_graduation_date()
        if graduation_date is not None:
            end_date_text = graduation_date.strftime("%d.%m.%Y")
        else:
            end_date_text = "Ausstehend"
        self.end_lbl = tk.Label(self.right_frame, text=end_date_text)
        self.end_label.grid(row=7, column=0, sticky="w")
        self.end_lbl.grid(row=7, column=1, sticky="e")
        self.expected_end_label = tk.Label(self.right_frame, text="Voraussichtlicher Abschluss:")
        self.controller.calc_expected_graduation_date()
        ex_graduation_date = self.controller.get_expected_graduation_date()
        if ex_graduation_date is not None:
            self.expected_end_lbl = tk.Label(self.right_frame, text=ex_graduation_date.strftime("%d.%m.%Y"))
        else:
            self.expected_end_lbl = tk.Label(self.right_frame, text="Ausstehend")
        self.expected_end_label.grid(row=8, column=0, sticky="w")
        self.expected_end_lbl.grid(row=8, column=1, sticky="e")

        self.graduate_label_color()

        # IU-Kontaktdaten
        self.contact_title = tk.Label(self.right_frame, text="IU Kontaktdaten", font=self.title_font)
        self.contact_title.grid(row=9, column=1, sticky="e", pady=15)

        self.advisory_label = tk.Label(self.right_frame, text="Studienberatung:")
        self.advisroy_lbl = tk.Label(self.right_frame, text=self.controller.iu_information.STUDY_ADVISORY_SERVICE)
        self.advisory_label.grid(row=10, column=0, sticky="w")
        self.advisroy_lbl.grid(row=10, column=1, sticky="e")

        self.exam_service_lable = tk.Label(self.right_frame, text="Prüfungsservice:")
        self.exam_service_lbl = tk.Label(self.right_frame, text=self.controller.iu_information.EXAM_SERVICE)
        self.exam_service_lable.grid(row=11, column=0, sticky="w")
        self.exam_service_lbl.grid(row=11, column=1, sticky="e")

        self.study_coach_label = tk.Label(self.right_frame, text="Study Coach:")
        self.study_coach_lbl = tk.Label(self.right_frame, text=self.controller.iu_information.STUDY_COACH)
        self.study_coach_label.grid(row=12, column=0, sticky="w")
        self.study_coach_lbl.grid(row=12, column=1, sticky="e")

        self.career_service_label = tk.Label(self.right_frame, text="Career Service:")

        self.career_service_lbl = tk.Label(self.right_frame, text=self.controller.iu_information.CAREER_SERVICE)
        self.career_service_label.grid(row=13, column=0, sticky="w")
        self.career_service_lbl.grid(row=13, column=1, sticky="e")

        # Student
        self.student_title = tk.Label(self.right_frame, text="Student", font=self.title_font)
        self.student_title.grid(row=14, column=1, sticky="e", pady=15)

        self.last_name_label = tk.Label(self.right_frame, text="Nachname:")
        self.last_name_lbl = tk.Label(self.right_frame, text=self.controller.student.last_name)
        self.last_name_label.grid(row=15, column=0, sticky="w")
        self.last_name_lbl.grid(row=15, column=1, sticky="e")

        self.first_name_label = tk.Label(self.right_frame, text="Vorname:")
        self.first_name_lbl = tk.Label(self.right_frame, text=self.controller.student.first_name)
        self.first_name_label.grid(row=16, column=0, sticky="w")
        self.first_name_lbl.grid(row=16, column=1, sticky="e")

        self.student_number_label = tk.Label(self.right_frame, text="Martrikelnummer:")
        self.student_number_lbl = tk.Label(self.right_frame, text=self.controller.student.number)
        self.student_number_label.grid(row=17, column=0, sticky="w")
        self.student_number_lbl.grid(row=17, column=1, sticky="e")

        self.refresh_button = tk.Button(self.right_frame, text="Aktualisieren", command=self.refresh_button_action)
        self.refresh_button.grid(row=18, column=1, sticky="e", pady=15)

    def on_closing(self):
        self.controller.cleanup()
        self.root.destroy()

    def create_module_elements(self):
        for modul in self.modules.values():
            if isinstance(modul, Modul):
                self.controller.load_modul(modul)
                modul_element = ModulElement(self.scrollable_frame, self.controller.student, modul, self)
                modul_element.frame.pack(pady=10)
            else:
                print(f"Unerwarteter Typ in module_list: {type(modul)}")

    def create_new_event(self):
        event_title = self.event_entry.get()
        event_date_str = self.event_date_entry.get()
        try:
            event_date = datetime.strptime(event_date_str, "%d.%m.%Y %H:%M")
            self.controller.create_event(event_title, event_date)
            self.create_event_elements()  # Aktualisieren der GUI-Elemente
            self.event_entry.delete(0, tk.END)
            self.event_date_entry.delete(0, tk.END)
        except ValueError as e:
            print(f"Fehler beim Erstellen des Events: {e}")

    def create_event_elements(self):
        for view in self.scrollable_frame_c.winfo_children():
            view.destroy()
        try:
            events = self.controller.get_events()
            if events is not None:
                for event in events:
                    EventElement(self.scrollable_frame_c, event,
                                 lambda event_id=event.event_id: self.controller.remove_event(event_id))
        except Exception as e:
            print(f"Fehler beim Laden der Termine: {e}")

    def graduate_label_color(self):
        self.controller.student.calc_is_expected_before_graduation()
        if self.controller.student.is_expected_before_graduation:
            self.expected_end_lbl.config(fg="green")
        else:
            self.expected_end_lbl.config(fg="red")

    def refresh_button_action(self):
        self.controller.set_planned_avg_grade(float(self.planned_grade_entry.get()))
        self.controller.calc_avg_grade()
        self.update_avg_grade_label()
        self.controller.save_avg_grade(self.controller.student)
        self.grade_label_color()

    def grade_label_color(self):
        self.controller.calc_avg_is_better_than_planned()
        if self.controller.get_avg_is_better_than_planned() is True:
            self.actual_grade_lbl.config(fg="green")
        elif self.controller.get_avg_is_better_than_planned() is False:
            self.actual_grade_lbl.config(fg="red")
        else:
            self.actual_grade_lbl.config(fg="black")

    def update_avg_grade_label(self):
        actual_avg_grade = self.controller.student.avg_grade.actual_avg_grade
        formatted_avg_grade = f"{actual_avg_grade:.1f}" if actual_avg_grade is not None else "Unbekannt"
        self.actual_grade_lbl.config(text=formatted_avg_grade)
        self.grade_label_color()

    def update_expected_graduation_date(self):
        if self.controller.student.expected_graduation_date is not None:
            self.expected_end_lbl.config(text=self.controller.student.expected_graduation_date.strftime("%d.%m.%Y"))

    def run(self):
        self.create_event_elements()
        self.update_avg_grade_label()
        self.root.mainloop()


if __name__ == "__main__":
    app = DashboardView()
    app.run()
