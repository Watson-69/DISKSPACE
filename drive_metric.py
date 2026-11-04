"""DriveMetric v2.0 — GUI front-end (cross-platform, pure Python + tkinter)."""
import os
import sys
import shutil
import heapq
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_TITLE = "DriveMetric"
APP_VERSION = "2.0"

FONT_UI = ("Segoe UI", 10)
FONT_UI_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUB = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 10)
FONT_MONO_BOLD = ("Consolas", 10, "bold")
FONT_BIG = ("Segoe UI", 18, "bold")
FONT_KPI = ("Segoe UI", 15, "bold")

THEMES = {
    "Dark Slate": {
        "bg": "#0F172A", "panel": "#1E293B", "card": "#1E293B", "fg": "#F8FAFC",
        "muted": "#94A3B8", "accent": "#06B6D4", "accent2": "#22D3EE",
        "entry_bg": "#0B1220", "button_bg": "#06B6D4", "button_hover": "#0891B2",
        "bar_crit": "#EF4444", "bar_warn": "#F59E0B", "bar_ok": "#22C55E",
        "bar_empty": "#334155", "title": "#F8FAFC", "border": "#334155",
        "success": "#22C55E", "danger": "#EF4444", "chart1": "#06B6D4",
        "chart2": "#334155",
    },
    "Neon Pink": {
        "bg": "#0F172A", "panel": "#1E293B", "card": "#1E293B", "fg": "#F8FAFC",
        "muted": "#94A3B8", "accent": "#EC4899", "accent2": "#F472B6",
        "entry_bg": "#0B1220", "button_bg": "#EC4899", "button_hover": "#DB2777",
        "bar_crit": "#EF4444", "bar_warn": "#F59E0B", "bar_ok": "#22C55E",
        "bar_empty": "#334155", "title": "#F8FAFC", "border": "#334155",
        "success": "#22C55E", "danger": "#EF4444", "chart1": "#EC4899",
        "chart2": "#334155",
    },
    "Matrix": {
        "bg": "#000000", "panel": "#0A1A0A", "card": "#0A1A0A", "fg": "#A7F3D0",
        "muted": "#6EE7B7", "accent": "#22C55E", "accent2": "#4ADE80",
        "entry_bg": "#020802", "button_bg": "#16A34A", "button_hover": "#15803D",
        "bar_crit": "#22C55E", "bar_warn": "#4ADE80", "bar_ok": "#22C55E",
        "bar_empty": "#14532D", "title": "#4ADE80", "border": "#14532D",
        "success": "#4ADE80", "danger": "#F87171", "chart1": "#22C55E",
        "chart2": "#14532D",
    },
    "Ocean": {
        "bg": "#07131F", "panel": "#0F2744", "card": "#0F2744", "fg": "#BAE6FD",
        "muted": "#7DD3FC", "accent": "#38BDF8", "accent2": "#7DD3FC",
        "entry_bg": "#050D16", "button_bg": "#0284C7", "button_hover": "#0369A1",
        "bar_crit": "#1D4ED8", "bar_warn": "#38BDF8", "bar_ok": "#7DD3FC",
        "bar_empty": "#1E3A5F", "title": "#7DD3FC", "border": "#1E3A5F",
        "success": "#7DD3FC", "danger": "#F87171", "chart1": "#38BDF8",
        "chart2": "#1E3A5F",
    },
    "Sunset": {
        "bg": "#120712", "panel": "#2A1226", "card": "#2A1226", "fg": "#FBCFE8",
        "muted": "#F9A8D4", "accent": "#EC4899", "accent2": "#F472B6",
        "entry_bg": "#0D040D", "button_bg": "#DB2777", "button_hover": "#BE185D",
        "bar_crit": "#EC4899", "bar_warn": "#F472B6", "bar_ok": "#A855F7",
        "bar_empty": "#3B1D3A", "title": "#F472B6", "border": "#3B1D3A",
        "success": "#A855F7", "danger": "#F87171", "chart1": "#EC4899",
        "chart2": "#3B1D3A",
    },
    "Light": {
        "bg": "#F1F5F9", "panel": "#FFFFFF", "card": "#FFFFFF", "fg": "#0F172A",
        "muted": "#475569", "accent": "#06B6D4", "accent2": "#0891B2",
        "entry_bg": "#F8FAFC", "button_bg": "#0891B2", "button_hover": "#0E7490",
        "bar_crit": "#DC2626", "bar_warn": "#CA8A04", "bar_ok": "#16A34A",
        "bar_empty": "#CBD5E1", "title": "#0F172A", "border": "#E2E8F0",
        "success": "#16A34A", "danger": "#DC2626", "chart1": "#0891B2",
        "chart2": "#CBD5E1",
    },
}

THEME_ORDER = ["Dark Slate", "Neon Pink", "Matrix", "Ocean", "Sunset", "Light"]

EXT_COLORS = ["#06B6D4", "#EC4899", "#F59E0B", "#22C55E", "#8B5CF6",
              "#F97316", "#14B8A6", "#EAB308", "#6366F1", "#EF4444"]


class DiskAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x760")
        self.minsize(980, 640)
        self.configure(bg="#0F172A")

        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"1180x760+{(sw-1180)//2}+{(sh-760)//2}")

        self.theme_name = tk.StringVar(value="Dark Slate")
        self.path_var = tk.StringVar(value=os.path.expanduser("~"))
        self.unit_var = tk.StringVar(value="GB")
        self.status_var = tk.StringVar(value="Ready. Pick a path and press Scan.")
        self.files_var = tk.StringVar(value="—")
        self.size_var = tk.StringVar(value="—")
        self.total_var = tk.StringVar(value="—")
        self.free_var = tk.StringVar(value="—")
        self.pct_var = tk.StringVar(value="—")
        self.advice_var = tk.StringVar(value="Run a scan to see storage insights.")
        self.target_var = tk.StringVar(value="—")
        self.scanning = False
        self._stop = False
        self._last_pct = 0.0
        self._t = THEMES["Dark Slate"]
        self._count = 0
        self._size = 0
        self._total = 0
        self._free = 0
        self._error = None
        self._done = True
        self._ext_sizes = {}
        self._top_files = []
        self._child_sizes = {}
        self._dir_sizes = {}
        self._top_files_list = []
        self._top_dirs_list = []
        self.view_mode = "files"
        self._tree_progress = 0.0
        self._animating = False

        self._build_ui()
        self.apply_theme(self.theme_name.get())

    def _build_ui(self):
        self.root_frame = tk.Frame(self, bg="#0F172A", bd=0, highlightthickness=0)
        self.root_frame.pack(fill="both", expand=True)

        # Header
        self.header = tk.Frame(self.root_frame, height=104, bd=0, highlightthickness=0, bg="#0F172A")
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        hdr = tk.Frame(self.header, bd=0, highlightthickness=0, bg="#0F172A")
        hdr.pack(fill="both", expand=True, padx=24)
        left = tk.Frame(hdr, bd=0, highlightthickness=0, bg="#0F172A")
        left.pack(side="left", fill="y")
        self.title_lbl = tk.Label(left, text="DriveMetric", font=FONT_TITLE, bg="#0F172A")
        self.title_lbl.pack(anchor="w", pady=(14, 0))
        self.subtitle_lbl = tk.Label(left, text="Native-speed storage insight  •  zero dependencies  •  consumer-friendly",
                                    font=FONT_SUB, bg="#0F172A")
        self.subtitle_lbl.pack(anchor="w", pady=(6, 14), ipady=6)
        right = tk.Frame(hdr, bd=0, highlightthickness=0, bg="#0F172A")
        right.pack(side="right", fill="y")
        self.version_lbl = tk.Label(right, text=f"v{APP_VERSION}", font=("Segoe UI", 9, "bold"), padx=10, pady=4, bg="#06B6D4", fg="#ffffff")
        self.version_lbl.pack(anchor="e", pady=(22, 0))
        self.accent_bar = tk.Frame(self.header, height=2, bd=0, highlightthickness=0, bg="#06B6D4")
        self.accent_bar.pack(fill="x", side="bottom")

        # Main split
        main = tk.Frame(self.root_frame, bg="#0F172A", bd=0, highlightthickness=0)
        main.pack(fill="both", expand=True, padx=16, pady=(12, 8))
        main.columnconfigure(0, weight=0, minsize=320)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = tk.Frame(main, width=320, bd=0, highlightthickness=1, relief="flat",
                                highlightbackground="#334155", highlightcolor="#334155", bg="#1E293B")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.sidebar.grid_propagate(False)
        self._build_sidebar()

        # Content
        self.content = tk.Frame(main, bg="#0F172A", bd=0, highlightthickness=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self._build_content()

        # Footer
        self.footer = tk.Frame(self.root_frame, height=30, bd=0, highlightthickness=0, bg="#0F172A")
        self.footer.pack(fill="x", side="bottom")
        self.footer.pack_propagate(False)
        self.footer_lbl = tk.Label(self.footer, text="DriveMetric v2.0 • MIT License • Built in Pure C + Python",
                                  font=("Segoe UI", 8), bd=0, bg="#0F172A", fg="#94A3B8")
        self.footer_lbl.pack(side="left", padx=16, pady=6)
        self.clock_lbl = tk.Label(self.footer, font=("Segoe UI", 8), bd=0, bg="#0F172A", fg="#94A3B8")
        self.clock_lbl.pack(side="right", padx=16, pady=6)
        self._tick_clock()

    def _build_sidebar(self):
        s = self.sidebar
        self._section(s, "📂  Target")
        path_row = tk.Frame(s, bd=0, highlightthickness=0, bg="#1E293B")
        path_row.pack(fill="x", pady=(4, 8), padx=10)
        self.path_entry = tk.Entry(path_row, textvariable=self.path_var, font=FONT_MONO, relief="flat", bd=0)
        self.path_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(8, 6))
        self.browse_btn = self._button(path_row, "Browse", self.browse, width=8)
        self.browse_btn.pack(side="right")

        self._section(s, "📏  Unit")
        unit_row = tk.Frame(s, bd=0, highlightthickness=0, bg="#1E293B")
        unit_row.pack(fill="x", pady=(4, 8), padx=10)
        for u in ("MB", "GB"):
            b = self._toggle_btn(unit_row, u, lambda v=u: self.unit_var.set(v))
            b.pack(side="left", padx=(0, 6))
            b._value = u
        self._unit_buttons = [w for w in unit_row.winfo_children() if isinstance(w, tk.Button)]
        self.unit_var.trace_add("write", lambda *a: self._update_unit_buttons())

        self._section(s, "🎨  Theme")
        self.theme_menu = tk.OptionMenu(s, self.theme_name, *THEME_ORDER, command=lambda v: self.apply_theme(v))
        self.theme_menu.config(font=FONT_UI, relief="flat", bd=0, highlightthickness=0, indicatoron=True)
        self.theme_menu.pack(fill="x", pady=(4, 8), padx=10, ipady=4)

        self._section(s, "⚡  Actions")
        self.scan_btn = self._button(s, "▶  Scan Now", self.start_scan, kind="primary")
        self.scan_btn.pack(fill="x", pady=(4, 6), padx=10)
        self.stop_btn = self._button(s, "■  Stop", self.stop_scan, kind="secondary", state="disabled")
        self.stop_btn.pack(fill="x", pady=(0, 8), padx=10)

        self._section(s, "⏳  Progress")
        self.progress = ttk.Progressbar(s, mode="indeterminate")
        self.progress.pack(fill="x", pady=(4, 4), padx=10)
        self.status_label = tk.Label(s, textvariable=self.status_var, font=FONT_UI, anchor="w", justify="left",
                                    wraplength=280, bg="#1E293B")
        self.status_label.pack(fill="x", pady=(4, 8), padx=10)

        self._section(s, "📊  Quick Stats")
        for label, var in (("Files", self.files_var), ("Size", self.size_var), ("Usage", self.pct_var)):
            row = tk.Frame(s, bd=0, highlightthickness=0, bg="#1E293B")
            row.pack(fill="x", pady=2, padx=10)
            tk.Label(row, text=label, font=FONT_UI_BOLD, bg="#1E293B", fg="#94A3B8").pack(side="left")
            tk.Label(row, textvariable=var, font=FONT_MONO_BOLD, bg="#1E293B", fg="#F8FAFC").pack(side="right")

    def _build_content(self):
        c = self.content
        # KPI row
        kpi = tk.Frame(c, bd=0, highlightthickness=0, bg="#0F172A")
        kpi.pack(fill="x", pady=(0, 10))
        for i in range(4):
            kpi.columnconfigure(i, weight=1)
        self._kpi_card(kpi, 0, "Files Found", self.files_var, "📄")
        self._kpi_card(kpi, 1, "Folder Size", self.size_var, "📦")
        self._kpi_card(kpi, 2, "Usage", self.pct_var, "📈")
        self._kpi_card(kpi, 3, "Free Space", self.free_var, "🟢")
        self._kpis = kpi

        # Charts row
        charts = tk.Frame(c, bd=0, highlightthickness=0, bg="#0F172A")
        charts.pack(fill="x", pady=(0, 10))
        charts.columnconfigure(0, weight=1)
        charts.columnconfigure(1, weight=1)

        # Left: Tree + target
        left_col = tk.Frame(charts, bd=0, highlightthickness=0, bg="#0F172A")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        dcard = tk.Frame(left_col, padx=12, pady=10, highlightthickness=1)
        dcard.pack(fill="x")
        tk.Label(dcard, text="Drive Usage", font=FONT_UI_BOLD).pack(anchor="w", pady=(0, 6))
        self.donut_canvas = tk.Canvas(dcard, height=260, highlightthickness=0, bd=0)
        self.donut_canvas.pack(fill="x")
        self.donut_canvas.bind("<Configure>", lambda e: self._draw_tree(1.0 if not getattr(self, "_animating", False) else self._tree_progress))

        tcard = tk.Frame(left_col, padx=12, pady=10, highlightthickness=1)
        tcard.pack(fill="x", pady=(10, 0))
        tk.Label(tcard, text="Target", font=FONT_UI_BOLD).pack(anchor="w")
        tk.Label(tcard, textvariable=self.target_var, font=FONT_MONO).pack(anchor="w", pady=(4, 0))
        tk.Label(tcard, textvariable=self.total_var, font=FONT_UI).pack(anchor="w", pady=(2, 0))
        self.advice_lbl = tk.Label(tcard, textvariable=self.advice_var, font=FONT_MONO_BOLD, anchor="w", justify="left")
        self.advice_lbl.pack(anchor="w", pady=(8, 0), fill="x")

        # Right: Top Folders
        fcard = tk.Frame(charts, padx=12, pady=10, highlightthickness=1)
        fcard.grid(row=0, column=1, sticky="nsew")
        tk.Label(fcard, text="Top Folders", font=FONT_UI_BOLD).pack(anchor="w", pady=(0, 6))
        self.folders_canvas = tk.Canvas(fcard, height=240, highlightthickness=0, bd=0)
        self.folders_canvas.pack(fill="both", expand=True)
        self.folders_canvas.bind("<Configure>", lambda e: self._draw_folders())

        # Lower section
        lower = tk.Frame(c, bd=0, highlightthickness=0, bg="#0F172A")
        lower.pack(fill="both", expand=True, pady=(0, 0))
        lower.columnconfigure(0, weight=1)
        lower.columnconfigure(1, weight=2)

        # File types
        tcard2 = tk.Frame(lower, padx=12, pady=10, highlightthickness=1)
        tcard2.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(tcard2, text="File Types (by size)", font=FONT_UI_BOLD).pack(anchor="w", pady=(0, 6))
        self.types_canvas = tk.Canvas(tcard2, height=160, highlightthickness=0, bd=0)
        self.types_canvas.pack(fill="x")
        self.types_canvas.bind("<Configure>", lambda e: self._draw_types())

        # Top items
        lcard = tk.Frame(lower, padx=12, pady=10, highlightthickness=1)
        lcard.grid(row=0, column=1, sticky="nsew")
        hdr_row = tk.Frame(lcard, bd=0, highlightthickness=0)
        hdr_row.pack(fill="x", pady=(0, 6))
        tk.Label(hdr_row, text="Top 10 Largest Items", font=FONT_UI_BOLD).pack(side="left")
        toggle = tk.Frame(hdr_row, bd=0, highlightthickness=0)
        toggle.pack(side="right")
        for mode, label in (("files", "Top Files"), ("dirs", "Top Directories"), ("combined", "Combined")):
            b = self._toggle_btn(toggle, label, lambda m=mode: self._set_view(m))
            b.pack(side="left", padx=(4, 0))
            b._mode = mode
        self._view_buttons = [w for w in toggle.winfo_children() if isinstance(w, tk.Button)]
        cols = ("#", "Name", "Directory", "Type", "Size")
        self.top_tree = ttk.Treeview(lcard, columns=cols, show="headings", height=8)
        self.top_tree.heading("#", text="#")
        self.top_tree.heading("Name", text="Name")
        self.top_tree.heading("Directory", text="Directory")
        self.top_tree.heading("Type", text="Type")
        self.top_tree.heading("Size", text="Size")
        self.top_tree.column("#", width=35, anchor="center")
        self.top_tree.column("Name", width=150)
        self.top_tree.column("Directory", width=260)
        self.top_tree.column("Type", width=70, anchor="center")
        self.top_tree.column("Size", width=100, anchor="e")
        sb = ttk.Scrollbar(lcard, orient="vertical", command=self.top_tree.yview)
        sb.pack(side="right", fill="y")
        self.top_tree.configure(yscrollcommand=sb.set)
        self.top_tree.pack(fill="both", expand=True, padx=(0, 16))
        self.top_tree.bind("<Double-1>", self._open_in_explorer)
        self.top_tree.bind("<Button-3>", self._open_in_explorer)
        self._row_paths = {}

        self._cards = [dcard, tcard, fcard, tcard2, lcard]
        self._kpis = kpi

    def _section(self, parent, title):
        lbl = tk.Label(parent, text=title, font=FONT_UI_BOLD)
        lbl.pack(anchor="w", pady=(10, 2), padx=10)
        return lbl

    def _button(self, parent, text, cmd, kind="secondary", width=None, state="normal"):
        btn = tk.Button(parent, text=text, command=cmd, font=FONT_UI_BOLD, relief="flat", bd=0,
                        cursor="hand2", padx=12, pady=7, state=state)
        if width:
            btn.configure(width=width)
        btn.bind("<Enter>", lambda e, b=btn: self._hover(b, True))
        btn.bind("<Leave>", lambda e, b=btn: self._hover(b, False))
        btn._kind = kind
        return btn

    def _hover(self, btn, on):
        t = self._t
        if btn._kind == "primary":
            btn.configure(bg=t["button_hover"] if on else t["button_bg"])
        else:
            btn.configure(bg=t["panel"] if on else t["card"])

    def _toggle_btn(self, parent, text, cmd):
        b = tk.Button(parent, text=text, command=cmd, font=FONT_UI, relief="flat", bd=0,
                      cursor="hand2", padx=10, pady=4)
        b._value = text
        return b

    def _update_unit_buttons(self):
        t = self._t
        for b in self._unit_buttons:
            sel = getattr(b, "_value", None) == self.unit_var.get()
            b.configure(bg=t["accent"] if sel else t["card"],
                        fg="#ffffff" if sel else t["fg"])

    def _kpi_card(self, parent, col, label, var, icon):
        card = tk.Frame(parent, padx=10, pady=8, highlightthickness=1)
        card.grid(row=0, column=col, padx=6, pady=4, sticky="nsew")
        tk.Label(card, text=f"{icon}  {label}", font=("Segoe UI", 9)).pack(anchor="w")
        tk.Label(card, textvariable=var, font=FONT_KPI).pack(anchor="w", pady=(4, 0))

    def _tick_clock(self):
        import datetime
        self.clock_lbl.configure(text=datetime.datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self._tick_clock)

    def apply_theme(self, name):
        t = THEMES[name]
        self._t = t
        self.configure(bg=t["bg"])
        self.root_frame.configure(bg=t["bg"])
        self.header.configure(bg=t["bg"])
        self.title_lbl.configure(bg=t["bg"], fg=t["title"])
        self.version_lbl.configure(bg=t["accent"], fg="#ffffff")
        self.subtitle_lbl.configure(bg=t["bg"], fg=t["muted"])
        self.accent_bar.configure(bg=t["accent"])
        self.sidebar.configure(bg=t["panel"], highlightbackground=t["border"], highlightcolor=t["border"])
        for w in self.sidebar.winfo_children():
            self._style_widget(w, t, is_sidebar=True)
        self.content.configure(bg=t["bg"])
        for card in self._cards:
            card.configure(bg=t["card"], highlightbackground=t["border"])
            for w in card.winfo_children():
                self._style_widget(w, t, is_card=True)
        for w in self._kpis.winfo_children():
            if isinstance(w, tk.Frame):
                w.configure(bg=t["card"], highlightbackground=t["border"])
                for c in w.winfo_children():
                    if isinstance(c, tk.Label):
                        f = str(c.cget("font"))
                        c.configure(bg=t["card"], fg=t["muted"] if "9" in f else t["fg"])
        self.path_entry.configure(bg=t["entry_bg"], fg=t["fg"], insertbackground=t["fg"],
                                 highlightbackground=t["border"], highlightthickness=1, highlightcolor=t["accent"])
        self.browse_btn.configure(bg=t["button_bg"], fg="#ffffff")
        self.theme_menu.configure(bg=t["entry_bg"], fg=t["fg"], activebackground=t["accent"],
                                 activeforeground="#ffffff", highlightbackground=t["border"],
                                 highlightthickness=1)
        self.theme_menu["menu"].configure(bg=t["entry_bg"], fg=t["fg"], activebackground=t["accent"],
                                         activeforeground="#ffffff", tearoff=0, borderwidth=0)
        self.scan_btn.configure(bg=t["button_bg"], fg="#ffffff")
        self.stop_btn.configure(bg=t["card"], fg=t["fg"])
        self.status_label.configure(bg=t["panel"], fg=t["muted"])
        self.advice_lbl.configure(bg=t["card"], fg=t["fg"])
        self.donut_canvas.configure(bg=t["card"])
        self.folders_canvas.configure(bg=t["card"])
        self.types_canvas.configure(bg=t["card"])
        for lbl in (self.footer_lbl, self.clock_lbl):
            lbl.configure(bg=t["bg"], fg=t["muted"])
        self._update_unit_buttons()
        for b in getattr(self, "_view_buttons", []):
            b.configure(bg=t["card"], fg=t["fg"])
        self._update_view_buttons()
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=t["card"], foreground=t["fg"],
                        fieldbackground=t["card"], bordercolor=t["border"], rowheight=24)
        style.configure("Treeview.Heading", background=t["panel"], foreground=t["fg"],
                        relief="flat", font=FONT_UI_BOLD)
        style.map("Treeview", background=[("selected", t["accent"])],
                  foreground=[("selected", "#ffffff")])
        style.configure("TCombobox", fieldbackground=t["entry_bg"], background=t["card"],
                        foreground=t["fg"], arrowcolor=t["fg"], bordercolor=t["border"])
        style.configure("TScrollbar", background=t["card"], troughcolor=t["bg"],
                        arrowcolor=t["muted"], bordercolor=t["bg"])
        style.configure("Horizontal.TProgressbar", troughcolor=t["card"], background=t["accent"],
                        bordercolor=t["card"])
        self._draw_tree(1.0)
        self._draw_folders()
        self._draw_types()

    def _style_widget(self, w, t, is_sidebar=False, is_card=False):
        if isinstance(w, (ttk.Widget, ttk.Combobox, ttk.Progressbar, ttk.Treeview, ttk.Scrollbar)):
            return
        bg = t["panel"] if is_sidebar else (t["card"] if is_card else t["bg"])
        if isinstance(w, tk.Label):
            f = str(w.cget("font"))
            w.configure(bg=bg, fg=t["muted"] if ("9" in f or "italic" in f) else t["fg"])
        elif isinstance(w, tk.Frame):
            w.configure(bg=bg)
            for c in w.winfo_children():
                self._style_widget(c, t, is_sidebar=is_sidebar, is_card=is_card)
        elif isinstance(w, tk.Entry):
            w.configure(bg=t["entry_bg"], fg=t["fg"], insertbackground=t["fg"])
        elif isinstance(w, tk.Button):
            kind = getattr(w, "_kind", "secondary")
            if kind == "primary":
                w.configure(bg=t["button_bg"], fg="#ffffff")
            else:
                w.configure(bg=t["card"], fg=t["fg"])
        elif isinstance(w, tk.Canvas):
            w.configure(bg=bg)

    def _start_tree_animation(self):
        self._tree_progress = 0.0
        self._animating = True
        self._anim_tick()

    def _anim_tick(self):
        if not self._animating:
            return
        self._tree_progress = min(1.0, self._tree_progress + 1.0 / 60.0)
        self._draw_tree(self._tree_progress)
        if self._tree_progress >= 1.0:
            self._animating = False
        else:
            self.after(16, self._anim_tick)

    def _draw_tree(self, p=1.0):
        c = self.donut_canvas
        c.delete("all")
        t = self._t
        w = c.winfo_width() or 300
        h = 230
        if not getattr(self, "_scanned", False):
            c.create_text(w / 2, h / 2, text="Run a scan to see storage breakdown", fill=t["muted"], font=FONT_UI)
            return
        total = self._total or 1
        used = total - self._free
        free = self._free
        pct = (used / total) * 100.0
        div = 1024 * 1024 * 1024
        cx = w / 2
        root_y = 14
        branch_y = 74
        used_x = cx - 70
        free_x = cx + 70
        node_h = 52
        node_w = 110
        child_y = 170

        def node(x, y, label, sub, color, fill):
            c.create_rectangle(x - node_w/2, y, x + node_w/2, y + node_h, fill=fill, outline=color, width=2)
            c.create_text(x, y + 10, text=label, fill=t["fg"], font=("Segoe UI", 9, "bold"))
            c.create_text(x, y + 24, text=sub, fill=t["muted"], font=("Segoe UI", 8))

        node(cx, root_y, "Total Drive", f"{total/div:.1f} GB", t["accent"], t["panel"])

        line_factor = min(p / 0.25, 1.0) if p > 0 else 0.0
        if line_factor > 0:
            rx, ry = cx, root_y + node_h
            for (tx, ty, color) in ((used_x, branch_y, t["chart1"]), (free_x, branch_y, t["bar_empty"])):
                ix = rx + (tx - rx) * line_factor
                iy = ry + (ty - ry) * line_factor
                c.create_line(rx, ry, ix, iy, fill=color, width=2, smooth=True)

        if p > 0.25:
            node(used_x, branch_y, "Used", f"{used/div:.1f} GB  {pct:.1f}%", t["chart1"], t["card"])
            node(free_x, branch_y, "Free", f"{free/div:.1f} GB  {100-pct:.1f}%", t["bar_empty"], t["card"])

        children = sorted(self._child_sizes.items(), key=lambda kv: kv[1], reverse=True)[:5]
        n = len(children)
        if n:
            span = min(w - 40, n * 95)
            start_x = cx - span / 2
            step = (span / (n - 1)) if n > 1 else 0
            child_xs = [start_x + i * step for i in range(n)] if n > 1 else [cx]
        else:
            child_xs = []
        child_factor_global = 0.0
        if p > 0.45:
            child_factor_global = min((p - 0.45) / 0.35, 1.0)
        if child_factor_global > 0 and n:
            ux, uy = used_x, branch_y + node_h
            for i, (name, sz) in enumerate(children):
                stagger = min(child_factor_global, max(0.0, (child_factor_global - i * 0.08) / 0.6))
                if stagger <= 0:
                    continue
                tx, ty = child_xs[i], child_y
                ix = ux + (tx - ux) * stagger
                iy = uy + (ty - uy) * stagger
                c.create_line(ux, uy, ix, iy, fill=t["chart1"], width=2, smooth=True)
        if p > 0.7 and n:
            for i, (name, sz) in enumerate(children):
                cx_i = child_xs[i]
                share = (sz / used * 100.0) if used else 0.0
                node(cx_i, child_y, name[:12], f"{sz/div:.1f} GB  {share:.1f}%", t["chart1"], t["card"])

    def _draw_folders(self):
        c = self.folders_canvas
        c.delete("all")
        t = self._t
        w = c.winfo_width() or 300
        h = c.winfo_height() or 200
        if not self._child_sizes:
            c.create_text(w/2, h/2, text="No data yet", fill=t["muted"], font=FONT_UI)
            return
        items = sorted(self._child_sizes.items(), key=lambda kv: kv[1], reverse=True)[:8]
        total = sum(v for _, v in items) or 1
        y = 6
        bar_h = 18
        gap = 6
        for i, (name, sz) in enumerate(items):
            yy = y + i * (bar_h + gap)
            if yy + bar_h > h:
                break
            c.create_text(6, yy + bar_h/2, text=name[:22], fill=t["fg"], font=("Segoe UI", 8), anchor="w")
            bx = 120
            bw = w - bx - 70
            frac = sz / total
            c.create_rectangle(bx, yy, bx + bw, yy + bar_h, fill=t["bar_empty"], outline="")
            c.create_rectangle(bx, yy, bx + int(bw * frac), yy + bar_h, fill=t["chart1"], outline="")
            unit = self.unit_var.get()
            div = 1024*1024 if unit == "MB" else 1024*1024*1024
            c.create_text(w - 6, yy + bar_h/2, text=f"{sz/div:.1f}{unit[0]}", fill=t["muted"],
                          font=("Segoe UI", 8), anchor="e")

    def _draw_types(self):
        c = self.types_canvas
        c.delete("all")
        t = self._t
        w = c.winfo_width() or 600
        h = 150
        if not self._ext_sizes:
            c.create_text(w/2, h/2, text="No data yet", fill=t["muted"], font=FONT_UI)
            return
        items = sorted(self._ext_sizes.items(), key=lambda kv: kv[1], reverse=True)[:8]
        total = sum(v for _, v in items) or 1
        cols = 2
        rows = (len(items) + 1) // cols
        cell_w = w // cols
        cell_h = h // max(rows, 1)
        for i, (ext, sz) in enumerate(items):
            col = i % cols
            row = i // cols
            x = col * cell_w + 6
            y = row * cell_h + 4
            frac = sz / total
            bw = cell_w - 80
            c.create_text(x, y + 8, text=ext, fill=t["fg"], font=("Segoe UI", 9, "bold"), anchor="w")
            c.create_rectangle(x, y + 18, x + bw, y + 30, fill=t["bar_empty"], outline="")
            color = EXT_COLORS[i % len(EXT_COLORS)]
            c.create_rectangle(x, y + 18, x + int(bw * frac), y + 30, fill=color, outline="")
            unit = self.unit_var.get()
            div = 1024*1024 if unit == "MB" else 1024*1024*1024
            c.create_text(x + bw + 4, y + 24, text=f"{sz/div:.1f}", fill=t["muted"],
                          font=("Segoe UI", 8), anchor="w")

    def browse(self):
        d = filedialog.askdirectory(initialdir=self.path_var.get() or os.path.expanduser("~"))
        if d:
            self.path_var.set(d)

    def start_scan(self):
        if self.scanning:
            return
        path = self.path_var.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("Invalid path", "The selected path does not exist.")
            return
        self.scanning = True
        self._stop = False
        self.scan_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.start(10)
        self.status_var.set("Scanning… 0 files")
        self.files_var.set("0")
        self.size_var.set("—")
        self.total_var.set("—")
        self.free_var.set("—")
        self.pct_var.set("—")
        self.advice_var.set("Scanning in progress…")
        self.target_var.set(path)
        self._count = 0
        self._size = 0
        self._ext_sizes = {}
        self._top_files = []
        self._child_sizes = {}
        self._dir_sizes = {}
        self._top_files_list = []
        self._top_dirs_list = []
        self._total = 0
        self._free = 0
        self._error = None
        self._done = False
        self._scanned = False
        t = threading.Thread(target=self._scan_worker, args=(path,), daemon=True)
        t.start()
        self._poll_thread(t)

    def stop_scan(self):
        self._stop = True

    def _scan_worker(self, path):
        try:
            for root, dirs, files in os.walk(path):
                if self._stop:
                    break
                self._dir_sizes.setdefault(root, 0)
                rel = os.path.relpath(root, path)
                top = rel.split(os.sep)[0] if rel != "." else None
                for f in files:
                    if self._stop:
                        break
                    fp = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(fp)
                    except OSError:
                        continue
                    self._size += sz
                    self._count += 1
                    ext = os.path.splitext(f)[1].lower() or "(no ext)"
                    self._ext_sizes[ext] = self._ext_sizes.get(ext, 0) + sz
                    heapq.heappush(self._top_files, (sz, fp))
                    if len(self._top_files) > 10:
                        heapq.heappop(self._top_files)
                    self._dir_sizes[root] = self._dir_sizes.get(root, 0) + sz
                    if top and top != ".":
                        self._child_sizes[top] = self._child_sizes.get(top, 0) + sz
                    else:
                        self._child_sizes["(root files)"] = self._child_sizes.get("(root files)", 0) + sz
            dirs_sorted = sorted(self._dir_sizes.keys(), key=lambda d: d.count(os.sep), reverse=True)
            for d in dirs_sorted:
                parent = os.path.dirname(d)
                if parent and parent in self._dir_sizes and parent != d:
                    self._dir_sizes[parent] += self._dir_sizes[d]
            try:
                du = shutil.disk_usage(path if os.path.isdir(path) else os.path.dirname(path))
                self._total = du.total
                self._free = du.free
            except Exception:
                self._total = 0
                self._free = 0
        except Exception as e:
            self._error = str(e)
        finally:
            self._done = True

    def _poll_thread(self, t):
        if not self._done:
            self.files_var.set(f"{self._count:,}")
            self.status_var.set(f"Scanning… {self._count:,} files  •  {self._size/(1024*1024):,.0f} MB")
            self.after(120, lambda: self._poll_thread(t))
        else:
            self._finish_scan()

    def _finish_scan(self):
        self.progress.stop()
        self.scanning = False
        self.scan_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if self._error:
            messagebox.showerror("Scan error", self._error)
            self.status_var.set("Error.")
            self.advice_var.set("Scan failed.")
            return
        count = self._count
        size = self._size
        total = self._total
        free = self._free
        self.files_var.set(f"{count:,}")
        divider = (1024 * 1024) if self.unit_var.get() == "MB" else (1024 * 1024 * 1024)
        unit = self.unit_var.get()
        self.size_var.set(f"{size / divider:,.2f} {unit}")
        self.target_var.set(self.path_var.get().strip())
        if total:
            used = total - free
            pct = (used / total) * 100.0
            self.total_var.set(f"{total / divider:,.1f} {unit}")
            self.free_var.set(f"{free / divider:,.1f} {unit}")
            self.pct_var.set(f"{pct:.1f}%")
            self._last_pct = pct
            t = self._t
            if pct > 90:
                self.advice_var.set("CRITICAL! Drive is almost full — free up space now.")
                self.advice_lbl.configure(fg=t["danger"])
            elif size > total * 0.5:
                self.advice_var.set("This folder alone uses over 50% of the drive!")
                self.advice_lbl.configure(fg=t["bar_warn"])
            else:
                self.advice_var.set("Everything looks good. Plenty of headroom.")
                self.advice_lbl.configure(fg=t["success"])
        else:
            self.pct_var.set("n/a")
            self.advice_var.set("Could not read drive data (permissions?).")
        self._scanned = True
        self._top_files_list = sorted(self._top_files, reverse=True)
        self._top_dirs_list = heapq.nlargest(10, self._dir_sizes.items(), key=lambda kv: kv[1])
        self._top_dirs_list = [(sz, p) for p, sz in self._top_dirs_list]
        self._refresh_table()
        self.status_var.set("Done." if not self._stop else "Stopped.")
        self._stop = False
        self._start_tree_animation()
        self._draw_folders()
        self._draw_types()

    def _set_view(self, mode):
        self.view_mode = mode
        self._update_view_buttons()
        self._refresh_table()

    def _update_view_buttons(self):
        t = self._t
        for b in getattr(self, "_view_buttons", []):
            sel = getattr(b, "_mode", None) == self.view_mode
            b.configure(bg=t["accent"] if sel else t["card"],
                        fg="#ffffff" if sel else t["fg"])

    def _truncate(self, text, n=46):
        if len(text) <= n:
            return text
        return text[: n // 2 - 2] + "…" + text[-(n // 2):]

    def _refresh_table(self):
        self.top_tree.delete(*self.top_tree.get_children())
        self._row_paths = {}
        if self.view_mode == "files":
            items = [(sz, p, "File") for sz, p in self._top_files_list]
        elif self.view_mode == "dirs":
            items = [(sz, p, "Folder") for sz, p in self._top_dirs_list]
        else:
            merged = [(sz, p, "File") for sz, p in self._top_files_list] + \
                     [(sz, p, "Folder") for sz, p in self._top_dirs_list]
            merged.sort(key=lambda x: x[0], reverse=True)
            items = merged[:10]
        div = 1024 * 1024 if self.unit_var.get() == "MB" else 1024 * 1024 * 1024
        unit = self.unit_var.get()
        for i, (sz, p, typ) in enumerate(items, 1):
            name = os.path.basename(p.rstrip("\\/")) or p
            parent = os.path.dirname(p.rstrip("\\/"))
            iid = self.top_tree.insert("", "end", values=(i, name, self._truncate(parent), typ, f"{sz/div:.2f} {unit}"))
            self._row_paths[iid] = p
        self._update_view_buttons()

    def _open_in_explorer(self, event=None):
        sel = self.top_tree.selection()
        if not sel:
            return
        path = self._row_paths.get(sel[0])
        if not path:
            return
        try:
            if os.name == "nt":
                if os.path.isdir(path):
                    os.startfile(path)
                else:
                    subprocess.Popen(["explorer", "/select,", path])
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path if os.path.isdir(path) else os.path.dirname(path)])
            else:
                subprocess.Popen(["xdg-open", path if os.path.isdir(path) else os.path.dirname(path)])
        except Exception as e:
            messagebox.showerror("Open failed", str(e))

    def destroy(self):
        super().destroy()


def main():
    app = DiskAnalyzerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
