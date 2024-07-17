import tkinter as tk


class EventElement:

    def __init__(self, parent, event_data, remove_callback):
        self.event = event_data
        self.remove_callback = remove_callback

        # Frame Termine-Element
        self.frame = tk.Frame(parent, width=450, height=30, padx=10, pady=10)
        self.frame.pack_propagate(False)
        self.frame.pack()

        # Label-Titel
        self.title_label = tk.Label(self.frame, text=self.event.event_title)
        self.exam_title_label = tk.Label(self.frame, text=f"Prüfungstermin: {self.event.event_title}")
        if self.event.is_exam_event:
            self.exam_title_label.grid(row=0, column=0, sticky="w")
        else:
            self.title_label.grid(row=0, column=0, sticky="w")

        # Label-Datum
        self.event_date = tk.Label(self.frame, text=self.event.event_date.strftime("%d.%m.%Y %H:%M"))
        self.event_date.grid(row=0, column=1, sticky="w")

        # Delete-Button
        self.delete_button = tk.Button(self.frame, text="Löschen", command=self.remove_event)
        self.delete_button.grid(row=0, column=2, sticky="e")

    def remove_event(self):
        self.remove_callback(self.event.event_id)
        self.frame.destroy()
