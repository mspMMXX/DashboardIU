import tkinter as tk
from tkinter import ttk
import os


def get_fill_status(status):
    if status == "Offen":
        return "gray"
    elif status == "In Bearbeitung":
        return "orange"
    else:
        return "green"


class ModulElement:

    def __init__(self, parent, student_modul):
        self.parent = parent
        self.student_modul = student_modul

        # Hauptframe
        self.frame = tk.Frame(parent, width=450, height=220, bg="#5F6E78", padx=10, pady=10)
        self.frame.pack_propagate(False)
        self.frame.pack(pady=10)

        # Linker Frame
        self.left_frame = tk.Frame(self.frame, width=150, height=200, bg="#5F6E78")
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Bild laden
        self.image_path = self.student_modul.image_path
        if not os.path.exists(self.image_path):
            self.image = None
        else:
            try:
                self.image = tk.PhotoImage(file=self.image_path)
            except Exception as e:
                self.image = None
                print(f"Fehler beim laden des Bildes: {e}")

        # Akronym und Bild
        self.acronym_label = tk.Label(self.left_frame, text=self.student_modul.acronym, bg="#5F6E78", fg="white")
        self.acronym_label.pack()

        self.modul_image = tk.Label(self.left_frame, image=self.image)
        self.modul_image.image = self.image
        self.modul_image.pack()

        # Rechter Frame - Modulinformationen
        self.right_frame = tk.Frame(self.frame, bg="5F6E78")
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=1, minsize=120)

        # Titel-Zeile
        self.title_label = tk.Label(self.right_frame, text=self.student_modul.title)
        self.title_label.grid(row=0, column=0, columnspace=2, sticky="w")

        # Status-Zeile
        self.status_oval = tk.Canvas(self.right_frame, width=25, height=25, bg="5F6E78", highlightthickness=0)
        self.status_oval.grid(row=1, column=0, sticky="w")
        fill_status = get_fill_status(self.student_modul.status)
        self.status_oval.create_oval(5, 5, 20, 20, fill=fill_status)
        self.status_oval.grid(row=1, column=0, sticky="w")

        self.status_var = tk.StringVar()
        self.status_var.set(self.student_modul.status)
        self.status_dropdown = ttk.Combobox(self.right_frame, textvariable=self.status_var)
        self.status_dropdown["values"] = ("Offen", "In Bearbeitung", "Abgeschlossen")
        self.status_dropdown.current(0)
        self.status_dropdown.bind("<<ComboboxSelected>>", self.update_modul)
        self.status_dropdown.grid(row=1, column=1, sticky="w")

        # Prüfungsform-Zeile
        self.exam_format_label = tk.Label(self.right_frame, text="Prüfungsform", bg="#5F6E78", fg="white")
        self.exam_format_label.grid(row=2, column=0, sticky="w")

        self.exam_format_dy_label = tk.Label(self.right_frame, text=self.student_modul.exam_format, bg="#5F6E78",
                                             fg="white")
        self.exam_format_dy_label.grid(row=2, column=1, sticky="w")

        # Startdatum-Zeile
        self.start_date_label = tk.Label(self.right_frame, text="Startdatum:", bg="#5F6E78", fg="white")
        self.start_date_label.grid(row=3, column=0, sticky="w")

        self.start_date_dy_label = tk.Label(self.right_frame, bg="#5F6E78", fg="white")
        if student_modul.start_date:
            self.start_date_dy_label.config(text=self.student_modul.start_date.strftime("%d.%m.%Y"))
        else:
            self.start_date_dy_label.config(text="Datum ausstehend", bg="#5F6E78", fg="white")
        self.start_date_dy_label.grid(row=3, column=1, sticky="w")

        # Enddatum-Zeile
        self.end_date_label = tk.Label(self.right_frame, text="Enddatum:", bg="#5F6E78", fg="white")
        self.end_date_label.grid(row=4, column=0, sticky="w")

        self.end_date_dy_label = tk.Label(self.right_frame, bg="#5F6E78", fg="white")
        if student_modul.end_date:
            self.end_date_dy_label.config(text=self.student_modul.end_date.strftime("%d.%m.%Y"))
        else:
            self.end_date_label.config(text="Datum ausstehend", bg="#5F6E78", fg="white")
        self.end_date_dy_label.grid(row=4, column=1, sticky="w")

        # Deadline-Zeile
        self.deadline_label = tk.Label(self.right_frame, text="Deadline:", bg="#5F6E78", fg="white")
        self.deadline_label.grid(row=5, column=0, sticky="w")

        self.deadline_dy_label = tk.Label(self.right_frame)
        if student_modul.deadline:
            self.deadline_dy_label.config(text=self.student_modul.deadline.strftime("%d.%m.%Y"))
        else:
            self.deadline_dy_label.config(text="Datum unbekannt", bg="#5F6E78", fg="white")
        self.deadline_dy_label.grid(row=5, column=1, sticky="w")

        # Prüfungsdatum-Zeile
        self.exam_date_label = tk.Label(self.right_frame, text="Prüfungstermin:", bg="#5F6E78", fg="white")
        self.exam_date_label.grid(row=6, column=0, sticky="w")

        self.exam_date_entry = tk.Entry(self.right_frame)
        if self.student_modul.exam_date:
            self.exam_date_entry.insert(0, self.student_modul.exam_format.strf("%d.%m.%Y %H:%M"))
        self.exam_date_entry.bind("<FocusOut>", self.update_modul)
        self.exam_date_entry.grid(row=6, column=1, sticky="w")

        # Noten-Zeile
        self.grade_label = tk.Label(self.right_frame, text="Note:", bg="#5F6E78", fg="white")
        self.grade_label.grid(row=7, column=0, sticky="w")

        self.grade_entry = tk.Entry(self.right_frame)
        if self.student_modul.grade is not None:
            self.grade_entry.insert(0, str(self.student_modul.grade))
        self.grade_entry.bind("<FocusOut>", self.update_modul)
        self.grade_entry.grid(row=7, column=1, sticky="w")

    def update_modul(self, event):
        new_status = self.status_var.get()
        self.student_modul.set_status(new_status)
        self.student_modul.set_start_date()
        self.student_modul.set_deadline()

        if new_status == "Abgeschlossen":
            self.student_modul.set_end_date()
        else:
            self.student_modul.end_date = None

        if new_status == "In Bearbeitung":
            if self.student_modul.start_date:
                self.start_date_dy_label.config(text=self.student_modul.start_date.strftime("%Y.%m.%d"))
            else:
                self.start_date_dy_label.config(text="Datum ausstehend")
            if self.student_modul.deadline:
                self.deadline_dy_label.config(text=self.student_modul.deadline.strftime("%Y.%m.%d"))
            else:
                self.deadline_dy_label.config(text="Datum unbekannt")
            if self.student_modul.end_date:
                self.end_date_dy_label.config(text=self.student_modul.end_date.strftime("%Y.%m.%d"))

        if self.student_modul.end_date:
            self.end_date_dy_label.config(text=self.student_modul.end_date.strftime("%Y.%m.%d"))
        else:
            self.end_date_dy_label.config(text="Datum ausstehend")

        exam_grade = self.grade_entry.get()
        if exam_grade != "":
            self.student_modul.set_grade(float(exam_grade))
