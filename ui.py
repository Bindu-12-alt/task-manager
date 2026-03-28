import tkinter as tk
from tkinter import ttk, messagebox
from task_manager import TaskManager
from task_dialog import TaskDialog

DARK_BLUE = "#1a3a5c"
SIDEBAR_HOVER = "#254d7a"
BG = "#f0f2f5"
WHITE = "#ffffff"
GREEN = "#27ae60"
RED = "#e74c3c"
ORANGE = "#e67e22"
TEXT = "#2c3e50"
SUBTEXT = "#7f8c8d"

PRIORITY_COLORS = {"High": RED, "Medium": ORANGE, "Low": GREEN}

NAV_ITEMS = [
    ("➕  Add Task", "add"),
    ("📋  All Tasks", "all"),
    ("✅  Completed", "completed"),
    ("⏳  Pending", "pending"),
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.manager = TaskManager()
        self.current_view = "all"
        self._build()
        self.refresh()

    def _build(self):
        # Header
        header = tk.Frame(self, bg=DARK_BLUE, height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Label(header, text="✔  Task Manager", bg=DARK_BLUE, fg=WHITE,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=24, pady=12)

        # Body
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(body, bg=DARK_BLUE, width=210)
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        # Main
        main = tk.Frame(body, bg=BG)
        main.pack(fill="both", expand=True, side="left")
        self._build_main(main)

    def _build_sidebar(self):
        tk.Label(self.sidebar, text="NAVIGATION", bg=DARK_BLUE, fg="#8ab4d4",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(24, 8))

        self.nav_buttons = {}
        for label, key in NAV_ITEMS:
            btn = tk.Label(self.sidebar, text=label, bg=DARK_BLUE, fg=WHITE,
                           font=("Segoe UI", 11), anchor="w", padx=20, pady=12,
                           cursor="hand2")
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, k=key: self._nav(k))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=SIDEBAR_HOVER))
            btn.bind("<Leave>", lambda e, b=btn, k=key: b.config(
                bg="#2d5f8a" if self.current_view == k else DARK_BLUE))
            self.nav_buttons[key] = btn

    def _build_main(self, parent):
        top_bar = tk.Frame(parent, bg=BG)
        top_bar.pack(fill="x", padx=24, pady=(20, 0))

        self.view_label = tk.Label(top_bar, text="All Tasks", bg=BG, fg=TEXT,
                                    font=("Segoe UI", 16, "bold"))
        self.view_label.pack(side="left")

        # Search
        search_frame = tk.Frame(top_bar, bg=WHITE, relief="flat",
                                 highlightbackground="#ddd", highlightthickness=1)
        search_frame.pack(side="right")
        tk.Label(search_frame, text="🔍", bg=WHITE, fg=SUBTEXT,
                 font=("Segoe UI", 11)).pack(side="left", padx=(10, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())
        tk.Entry(search_frame, textvariable=self.search_var, bd=0, bg=WHITE,
                 fg=TEXT, font=("Segoe UI", 10), width=22,
                 insertbackground=TEXT).pack(side="left", pady=8, padx=(0, 10))

        # Scrollable task area
        container = tk.Frame(parent, bg=BG)
        container.pack(fill="both", expand=True, padx=24, pady=16)

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.task_frame = tk.Frame(canvas, bg=BG)

        self.task_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    def _nav(self, key):
        if key == "add":
            self._open_add()
            return
        self.current_view = key
        self._update_nav_highlight()
        labels = {"all": "All Tasks", "completed": "Completed Tasks", "pending": "Pending Tasks"}
        self.view_label.config(text=labels[key])
        self.refresh()

    def _update_nav_highlight(self):
        for k, btn in self.nav_buttons.items():
            btn.config(bg="#2d5f8a" if k == self.current_view else DARK_BLUE)

    def refresh(self):
        for w in self.task_frame.winfo_children():
            w.destroy()
        tasks = self.manager.get_filtered(self.current_view, self.search_var.get())
        if not tasks:
            tk.Label(self.task_frame, text="No tasks found.", bg=BG, fg=SUBTEXT,
                     font=("Segoe UI", 12)).pack(pady=40)
            return
        for task in tasks:
            self._task_card(task)

    def _task_card(self, task):
        card = tk.Frame(self.task_frame, bg=WHITE, relief="flat",
                        highlightbackground="#e0e0e0", highlightthickness=1)
        card.pack(fill="x", pady=6, ipady=4)

        # Priority stripe
        stripe = tk.Frame(card, bg=PRIORITY_COLORS[task.priority], width=5)
        stripe.pack(side="left", fill="y")

        content = tk.Frame(card, bg=WHITE)
        content.pack(side="left", fill="both", expand=True, padx=16, pady=12)

        # Row 1: title + priority badge
        row1 = tk.Frame(content, bg=WHITE)
        row1.pack(fill="x")

        title_font = ("Segoe UI", 12, "bold")
        title_text = f"✓ {task.title}" if task.completed else task.title
        title_color = SUBTEXT if task.completed else TEXT
        tk.Label(row1, text=title_text, bg=WHITE, fg=title_color,
                 font=title_font).pack(side="left")

        badge_color = PRIORITY_COLORS[task.priority]
        badge = tk.Label(row1, text=task.priority, bg=badge_color, fg=WHITE,
                         font=("Segoe UI", 8, "bold"), padx=8, pady=2)
        badge.pack(side="left", padx=10)

        # Row 2: description
        if task.description:
            tk.Label(content, text=task.description, bg=WHITE, fg=SUBTEXT,
                     font=("Segoe UI", 10), anchor="w", wraplength=600,
                     justify="left").pack(fill="x", pady=(4, 0))

        # Row 3: due date
        if task.due_date:
            tk.Label(content, text=f"📅  Due: {task.due_date}", bg=WHITE, fg=SUBTEXT,
                     font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))

        # Action buttons
        btn_frame = tk.Frame(card, bg=WHITE)
        btn_frame.pack(side="right", padx=16, pady=12)

        if not task.completed:
            self._action_btn(btn_frame, "Complete", GREEN, lambda t=task: self._complete(t.id))
        self._action_btn(btn_frame, "Edit", "#3498db", lambda t=task: self._open_edit(t))
        self._action_btn(btn_frame, "Delete", RED, lambda t=task: self._delete(t.id))

    def _action_btn(self, parent, text, color, cmd):
        btn = tk.Button(parent, text=text, command=cmd, bg=color, fg=WHITE,
                        font=("Segoe UI", 9, "bold"), relief="flat",
                        padx=10, pady=5, cursor="hand2",
                        activebackground=color, activeforeground=WHITE)
        btn.pack(side="left", padx=3)
        btn.bind("<Enter>", lambda e: btn.config(bg=self._darken(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    def _darken(self, hex_color):
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        return f"#{max(r-30,0):02x}{max(g-30,0):02x}{max(b-30,0):02x}"

    def _open_add(self):
        def save(title, desc, priority, due_date):
            self.manager.add(title, desc, priority, due_date)
            self.current_view = "all"
            self.view_label.config(text="All Tasks")
            self._update_nav_highlight()
            self.refresh()
        TaskDialog(self, save)

    def _open_edit(self, task):
        def save(title, desc, priority, due_date):
            self.manager.update(task.id, title, desc, priority, due_date)
            self.refresh()
        TaskDialog(self, save, task)

    def _complete(self, id):
        self.manager.complete(id)
        self.refresh()

    def _delete(self, id):
        if messagebox.askyesno("Delete", "Delete this task?"):
            self.manager.delete(id)
            self.refresh()
