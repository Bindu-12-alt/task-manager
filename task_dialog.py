import tkinter as tk
from tkinter import ttk, messagebox

PRIORITIES = ["High", "Medium", "Low"]

class TaskDialog(tk.Toplevel):
    def __init__(self, parent, on_save, task=None):
        super().__init__(parent)
        self.on_save = on_save
        self.task = task
        self.title("Edit Task" if task else "Add Task")
        self.resizable(False, False)
        self.configure(bg="#ffffff")
        self.grab_set()
        self._build()
        self._center(parent)

    def _center(self, parent):
        self.update_idletasks()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{px + (pw - w)//2}+{py + (ph - h)//2}")

    def _field(self, parent, label, row):
        tk.Label(parent, text=label, bg="#ffffff", fg="#333", font=("Segoe UI", 10, "bold")).grid(
            row=row, column=0, sticky="w", pady=(10, 2))

    def _build(self):
        pad = {"padx": 30, "pady": 5}
        frame = tk.Frame(self, bg="#ffffff")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        tk.Label(frame, text="Edit Task" if self.task else "Add New Task",
                 bg="#ffffff", fg="#1a3a5c", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 5))

        self._field(frame, "Title *", 1)
        self.title_var = tk.StringVar(value=self.task.title if self.task else "")
        ttk.Entry(frame, textvariable=self.title_var, width=40,
                  font=("Segoe UI", 10)).grid(row=2, column=0, padx=30, sticky="ew")

        self._field(frame, "Description", 3)
        self.desc_text = tk.Text(frame, width=40, height=4, font=("Segoe UI", 10),
                                  relief="solid", bd=1, fg="#333")
        self.desc_text.grid(row=4, column=0, padx=30, sticky="ew")
        if self.task:
            self.desc_text.insert("1.0", self.task.description)

        self._field(frame, "Priority", 5)
        self.priority_var = tk.StringVar(value=self.task.priority if self.task else "Medium")
        priority_cb = ttk.Combobox(frame, textvariable=self.priority_var,
                                    values=PRIORITIES, state="readonly", width=38,
                                    font=("Segoe UI", 10))
        priority_cb.grid(row=6, column=0, padx=30, sticky="ew")

        self._field(frame, "Due Date (YYYY-MM-DD)", 7)
        self.date_var = tk.StringVar(value=self.task.due_date if self.task else "")
        ttk.Entry(frame, textvariable=self.date_var, width=40,
                  font=("Segoe UI", 10)).grid(row=8, column=0, padx=30, sticky="ew")

        # Buttons
        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.grid(row=9, column=0, padx=30, pady=20, sticky="e")

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.destroy,
                               bg="#e0e0e0", fg="#333", font=("Segoe UI", 10),
                               relief="flat", padx=16, pady=8, cursor="hand2")
        cancel_btn.pack(side="left", padx=(0, 10))

        save_btn = tk.Button(btn_frame, text="Save Task", command=self._save,
                             bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"),
                             relief="flat", padx=16, pady=8, cursor="hand2",
                             activebackground="#219a52", activeforeground="white")
        save_btn.pack(side="left")

    def _save(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Title is required.", parent=self)
            return
        self.on_save(
            title,
            self.desc_text.get("1.0", "end").strip(),
            self.priority_var.get(),
            self.date_var.get().strip()
        )
        self.destroy()
