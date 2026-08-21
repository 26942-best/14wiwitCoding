# -*- coding: utf-8 -*-
"""
Academic Guidance - Windows Desktop
Tkinter + SQLite (Modernized UI + Task Management)

Run:
    python 14wallahi.py
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, font
from pathlib import Path

# Force database to save directly in the Downloads folder
DB_PATH = "academic_guidance.db"

# Modern Slate / Indigo Palette
COLORS = {
    "sidebar_bg": "#0f172a",       # Slate 900
    "sidebar_card": "#1e293b",     # Slate 800
    "sidebar_hover": "#334155",    # Slate 700
    "active_pill": "#38bdf8",      # Sky 400
    "active_text": "#ffffff",
    "nav_text": "#94a3b8",          # Slate 400
    "bg": "#f8fafc",               # Slate 50
    "card_bg": "#ffffff",
    "card_border": "#e2e8f0",      # Slate 200
    "text_dark": "#0f172a",        # Slate 900
    "text_muted": "#64748b",       # Slate 500
    "accent": "#2563eb",           # Blue 600
    "accent_hover": "#1d4ed8",     # Blue 700
    "row_even": "#ffffff",
    "row_odd": "#f8fafc",
    "success": "#10b981",
    "warning": "#f59e0b",
}

NAV = [
    ("home", "⌂", "หน้าหลัก"),
    ("plan", "▣", "แผนการเรียน"),
    ("courses", "▤", "รายวิชา"),
    ("grades", "▥", "ผลการเรียน"),
    ("portfolio", "□", "ช่วยทำ Portfolio"),
    ("careers", "◎", "แนะแนวอาชีพ"),
    ("settings", "⚙", "ตั้งค่า"),
]


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        self.seed_data()

    def create_tables(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            student_class TEXT,
            study_plan TEXT,
            student_code TEXT,
            advisor_name TEXT,
            target_university TEXT,
            target_gpax REAL DEFAULT 3.50,
            gpax REAL DEFAULT 0.00,
            total_credits INTEGER DEFAULT 42,
            credits_earned INTEGER DEFAULT 28,
            current_term TEXT DEFAULT '',
            school_name TEXT,
            system_name TEXT DEFAULT 'ระบบแนะแนวการเรียน'
        );

        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            name TEXT,
            category TEXT,
            credits REAL,
            status TEXT
        );

        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT,
            code TEXT,
            name TEXT,
            category TEXT,
            credits REAL,
            grade TEXT,
            status TEXT
        );

        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            level TEXT,
            period TEXT,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            faculty TEXT,
            match_rate INTEGER,
            description TEXT,
            subjects TEXT
        );

        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            percentage INTEGER
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            detail TEXT,
            status TEXT,
            status_color TEXT
        );
        """)
        self.conn.commit()

    def seed_data(self):
        cur = self.conn.cursor()

        if cur.execute("SELECT COUNT(*) FROM profile").fetchone()[0] == 0:
            cur.execute("""
                INSERT INTO profile (
                    id, student_name, student_class, study_plan,
                    student_code, advisor_name, target_university,
                    target_gpax, gpax, total_credits, credits_earned,
                    current_term, school_name, system_name
                )
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "sigma", "ม.4/4", "เตรียมวิศวกรรมศาสตร์", "48920",
                "อ.สมศักดิ์ ปิ่นมณี", "คณะวิศวกรรมศาสตร์",
                3.50, 3.45, 42, 28, "ม.4 เทอม 1",
                "โรงเรียนบดินทรเดชา", "ระบบแนะแนวการเรียน"
            ))

        if cur.execute("SELECT COUNT(*) FROM courses").fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO courses (code, name, category, credits, status)
                VALUES (?, ?, ?, ?, ?)
            """, [
                ("ว30281", "ฟิสิกส์ 1 (กลศาสตร์)", "วิทยาศาสตร์", 1.5, "กำลังศึกษา"),
                ("ค30221", "คณิตศาสตร์เพิ่มเติม 3", "คณิตศาสตร์", 2.0, "กำลังศึกษา"),
                ("ว30201", "เคมีเบื้องต้น 1", "วิทยาศาสตร์", 1.5, "กำลังศึกษา"),
                ("อ30205", "ภาษาอังกฤษเชิงวิชาการ", "ภาษาอังกฤษ", 1.0, "กำลังศึกษา"),
                ("ง30211", "การเขียนโปรแกรมและการควบคุม", "เทคโนโลยี", 1.0, "กำลังศึกษา"),
            ])

        if cur.execute("SELECT COUNT(*) FROM grades").fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO grades (term, code, name, category, credits, grade, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                ("ม.4 เทอม 1", "ว30101", "ฟิสิกส์เบื้องต้น", "วิทยาศาสตร์", 1.5, "4.0", "ดีเยี่ยม"),
                ("ม.4 เทอม 1", "ค30101", "คณิตศาสตร์พื้นฐาน", "คณิตศาสตร์", 1.5, "3.5", "ดีมาก"),
                ("ม.4 เทอม 1", "อ30101", "ภาษาอังกฤษ", "ภาษาอังกฤษ", 1.0, "4.0", "ดีเยี่ยม"),
                ("ม.4 เทอม 2", "ว30102", "เคมีเบื้องต้น", "วิทยาศาสตร์", 1.5, "4.0", "ดีเยี่ยม"),
                ("ม.4 เทอม 2", "ค30102", "คณิตศาสตร์พื้นฐาน 2", "คณิตศาสตร์", 1.5, "3.5", "ดีมาก"),
            ])

        if cur.execute("SELECT COUNT(*) FROM portfolio").fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO portfolio (title, category, level, period, description)
                VALUES (?, ?, ?, ?, ?)
            """, [
                ("รางวัลชนะเลิศ การแข่งขันหุ่นยนต์", "การแข่งขันวิชาการ", "ระดับภาค", "ส.ค. 2567", "การแข่งขันหุ่นยนต์"),
                ("ค่ายโอลิมปิกวิชาการ สอวน.", "การแข่งขันวิชาการ", "ระดับภาค", "มิ.ย. 2567", "สาขาฟิสิกส์"),
                ("โครงงานระบบ IoT", "โครงงาน", "ระดับโรงเรียน", "พ.ค. 2567", "ระบบ IoT แจ้งเตือนมลพิษ"),
            ])

        if cur.execute("SELECT COUNT(*) FROM careers").fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO careers (name, faculty, match_rate, description, subjects)
                VALUES (?, ?, ?, ?, ?)
            """, [
                ("วิศวกรปัญญาประดิษฐ์ (AI Engineer)", "วิศวกรรมคอมพิวเตอร์", 96, "พัฒนาและเทรนโมเดล Machine Learning", "คณิตศาสตร์ · ฟิสิกส์ · Programming"),
                ("นักวิทยาศาสตร์ข้อมูล", "วิทยาการข้อมูล", 92, "วิเคราะห์ข้อมูลและสร้างโมเดลพยากรณ์", "คณิตศาสตร์ · Statistics · Programming"),
                ("วิศวกรหุ่นยนต์และ IoT", "วิศวกรรมเมคทรอนิกส์", 88, "ออกแบบระบบหุ่นยนต์และระบบ IoT", "ฟิสิกส์ · Electronics · Programming"),
                ("นักพัฒนาซอฟต์แวร์", "วิทยาการคอมพิวเตอร์", 85, "พัฒนาเว็บไซต์ แอป และระบบซอฟต์แวร์", "Programming · Computer Science"),
            ])

        if cur.execute("SELECT COUNT(*) FROM progress").fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO progress (subject, percentage) VALUES (?, ?)
            """, [
                ("คณิตศาสตร์", 80),
                ("วิทยาศาสตร์", 72),
                ("ภาษาอังกฤษ", 65),
                ("วิศวกรรมและเทคโนโลยี", 58),
                ("สังคมศึกษา", 70),
            ])

        if cur.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO tasks (title, detail, status, status_color)
                VALUES (?, ?, ?, ?)
            """, [
                ("รายงานผลการทดลองการเคลื่อนที่", "ฟิสิกส์ 1 · ส่งพรุ่งนี้", "ด่วน", "#f59e0b"),
                ("โครงงาน Arduino Smart Home", "การเขียนโปรแกรม · ส่ง 10 พ.ย.", "กำลังทำ", "#2563eb"),
                ("บทความวิชาการภาษาอังกฤษ", "ภาษาอังกฤษ · ส่ง 15 พ.ย.", "รอดำเนินการ", "#64748b"),
            ])

        self.conn.commit()

    def one(self, sql, values=()):
        return self.conn.execute(sql, values).fetchone()

    def all(self, sql, values=()):
        return self.conn.execute(sql, values).fetchall()

    def commit(self):
        self.conn.commit()


class ModernButton(tk.Frame):
    """Custom flat button with hover animations."""
    def __init__(self, parent, text, command=None, bg=COLORS["accent"], fg="white", hover_bg=COLORS["accent_hover"], font_tuple=("Segoe UI", 10, "bold"), **kwargs):
        super().__init__(parent, bg=bg, cursor="hand2", **kwargs)
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg

        self.label = tk.Label(self, text=text, bg=bg, fg=fg, font=font_tuple, padx=12, pady=6)
        self.label.pack(fill="both", expand=True)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.label.bind("<Enter>", self.on_enter)
        self.label.bind("<Leave>", self.on_leave)
        self.label.bind("<Button-1>", self.on_click)

    def on_enter(self, e):
        self.configure(bg=self.hover_bg)
        self.label.configure(bg=self.hover_bg)

    def on_leave(self, e):
        self.configure(bg=self.bg)
        self.label.configure(bg=self.bg)

    def on_click(self, e):
        if self.command:
            self.command()


class AcademicGuidance(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.title("ระบบแนะแนวการเรียน - Academic Guidance System")
        self.geometry("1300x820")
        self.minsize(1050, 680)
        self.configure(bg=COLORS["bg"])

        available_fonts = font.families()
        self.font_family = "Segoe UI" if "Segoe UI" in available_fonts else "Tahoma"

        self.setup_styles()

        self.sidebar = tk.Frame(self, bg=COLORS["sidebar_bg"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main = tk.Frame(self, bg=COLORS["bg"])
        self.main.pack(side="left", fill="both", expand=True)

        self.buttons = {}
        self.current_page = None
        self.create_sidebar()
        self.show_page("home")

    def setup_styles(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "Treeview",
            background=COLORS["card_bg"],
            foreground=COLORS["text_dark"],
            rowheight=38,
            font=(self.font_family, 10),
            fieldbackground=COLORS["card_bg"],
            borderwidth=0,
        )
        self.style.configure(
            "Treeview.Heading",
            background=COLORS["bg"],
            foreground=COLORS["text_muted"],
            font=(self.font_family, 9, "bold"),
            borderwidth=0,
            padding=10,
        )
        self.style.map("Treeview", background=[("selected", "#e0f2fe")], foreground=[("selected", COLORS["accent"])])

    # ---------------- SIDEBAR ----------------

    def create_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        profile = self.db.one("SELECT * FROM profile WHERE id=1")

        brand = tk.Frame(self.sidebar, bg=COLORS["sidebar_bg"], pady=24, padx=20)
        brand.pack(fill="x")

        logo_box = tk.Frame(brand, bg=COLORS["accent"], width=42, height=42)
        logo_box.pack(side="left")
        logo_box.pack_propagate(False)

        tk.Label(
            logo_box, text="🎓", font=("Segoe UI Emoji", 16), bg=COLORS["accent"], fg="white"
        ).pack(expand=True)

        info = tk.Frame(brand, bg=COLORS["sidebar_bg"])
        info.pack(side="left", fill="x", padx=(12, 0))

        tk.Label(
            info,
            text=profile["system_name"],
            font=(self.font_family, 11, "bold"),
            bg=COLORS["sidebar_bg"],
            fg="white",
        ).pack(anchor="w")

        tk.Label(
            info,
            text=profile["school_name"],
            font=(self.font_family, 8),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["nav_text"],
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(self.sidebar, bg=COLORS["sidebar_card"], height=1).pack(fill="x", padx=16, pady=(0, 16))

        self.buttons = {}
        for key, icon, text in NAV:
            btn_frame = tk.Frame(self.sidebar, bg=COLORS["sidebar_bg"], cursor="hand2")
            btn_frame.pack(fill="x", padx=12, pady=3)

            indicator = tk.Frame(btn_frame, bg=COLORS["sidebar_bg"], width=4, height=36)
            indicator.pack(side="left")

            label = tk.Label(
                btn_frame,
                text=f"  {icon}    {text}",
                anchor="w",
                font=(self.font_family, 10),
                bg=COLORS["sidebar_bg"],
                fg=COLORS["nav_text"],
                pady=10,
            )
            label.pack(side="left", fill="x", expand=True, padx=(8, 0))

            for widget in (btn_frame, label):
                widget.bind("<Enter>", lambda e, k=key: self.on_nav_hover(k, True))
                widget.bind("<Leave>", lambda e, k=key: self.on_nav_hover(k, False))
                widget.bind("<Button-1>", lambda e, k=key: self.show_page(k))

            self.buttons[key] = {"frame": btn_frame, "label": label, "indicator": indicator}

    def on_nav_hover(self, key, is_hover):
        if self.current_page == key:
            return
        bg = COLORS["sidebar_hover"] if is_hover else COLORS["sidebar_bg"]
        fg = "white" if is_hover else COLORS["nav_text"]
        self.buttons[key]["frame"].configure(bg=bg)
        self.buttons[key]["label"].configure(bg=bg, fg=fg)

    # ---------------- PAGE SYSTEM ----------------

    def clear_page(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def show_page(self, page):
        self.current_page = page

        for key, btn in self.buttons.items():
            if key == page:
                btn["frame"].configure(bg=COLORS["sidebar_card"])
                btn["label"].configure(bg=COLORS["sidebar_card"], fg=COLORS["active_pill"], font=(self.font_family, 10, "bold"))
                btn["indicator"].configure(bg=COLORS["active_pill"])
            else:
                btn["frame"].configure(bg=COLORS["sidebar_bg"])
                btn["label"].configure(bg=COLORS["sidebar_bg"], fg=COLORS["nav_text"], font=(self.font_family, 10))
                btn["indicator"].configure(bg=COLORS["sidebar_bg"])

        self.clear_page()

        pages = {
            "home": self.home_page,
            "plan": self.plan_page,
            "courses": self.courses_page,
            "grades": self.grades_page,
            "portfolio": self.portfolio_page,
            "careers": self.careers_page,
            "settings": self.settings_page,
        }
        pages[page]()

    # ---------------- COMMON GUI COMPONENTS ----------------

    def header(self, title):
        profile = self.db.one("SELECT * FROM profile WHERE id=1")

        bar = tk.Frame(self.main, bg=COLORS["card_bg"], height=64)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(
            bar,
            text=title,
            font=(self.font_family, 15, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(side="left", padx=28, pady=18)

        user_box = tk.Frame(bar, bg=COLORS["bg"], padx=12, pady=6)
        user_box.pack(side="right", padx=28)

        tk.Label(
            user_box, text="👤", font=("Segoe UI Emoji", 10), bg=COLORS["bg"]
        ).pack(side="left", padx=(0, 6))

        tk.Label(
            user_box,
            text=f"{profile['student_name']} ({profile['student_class']})",
            font=(self.font_family, 9, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text_dark"],
        ).pack(side="left")

        tk.Frame(self.main, bg=COLORS["card_border"], height=1).pack(fill="x")

    def content(self):
        frame = tk.Frame(self.main, bg=COLORS["bg"])
        frame.pack(fill="both", expand=True, padx=28, pady=24)
        return frame

    def card(self, parent, padding=20):
        outer = tk.Frame(parent, bg=COLORS["card_border"], bd=0)
        inner = tk.Frame(outer, bg=COLORS["card_bg"], padx=padding, pady=padding)
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        return outer, inner

    def stat_card(self, parent, title, value, description="", accent_color=COLORS["accent"]):
        outer, inner = self.card(parent, padding=16)
        outer.pack(side="left", fill="both", expand=True, padx=6)

        accent_bar = tk.Frame(inner, bg=accent_color, height=3)
        accent_bar.pack(fill="x", pady=(0, 10))

        tk.Label(
            inner,
            text=title,
            font=(self.font_family, 9, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_muted"],
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=value,
            font=(self.font_family, 22, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w", pady=(4, 2))

        if description:
            tk.Label(
                inner,
                text=description,
                font=(self.font_family, 8),
                bg=COLORS["card_bg"],
                fg=COLORS["text_muted"],
            ).pack(anchor="w")

    def draw_progress_bar(self, parent, percentage, color=COLORS["accent"]):
        canvas = tk.Canvas(parent, height=10, bg="#e2e8f0", highlightthickness=0)
        canvas.pack(fill="x", expand=True, pady=(4, 8))

        def update_bar(event):
            canvas.delete("all")
            w = event.width
            fill_w = max(0, int(w * percentage / 100))
            canvas.create_rectangle(0, 0, fill_w, 10, fill=color, width=0)

        canvas.bind("<Configure>", update_bar)

    def create_table(self, parent, rows, columns):
        outer, inner = self.card(parent, padding=0)
        outer.pack(fill="both", expand=True)

        keys = [x[0] for x in columns]

        tree = ttk.Treeview(inner, columns=keys, show="headings", selectmode="browse")

        for key, title in columns:
            tree.heading(key, text=title.upper())
            tree.column(key, width=140, anchor="w")

        tree.tag_configure("even", background=COLORS["row_even"])
        tree.tag_configure("odd", background=COLORS["row_odd"])

        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=[row[key] for key in keys], tags=(tag,))

        scrollbar = ttk.Scrollbar(inner, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------------- HOME ----------------

    def home_page(self):
        self.header("หน้าหลัก")
        content = self.content()
        profile = self.db.one("SELECT * FROM profile WHERE id=1")

        banner_outer, banner_inner = self.card(content, padding=20)
        banner_outer.pack(fill="x", pady=(0, 20))

        tk.Label(
            banner_inner,
            text=f"ยินดีต้อนรับกลับ, {profile['student_name']} 👋",
            font=(self.font_family, 16, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w")

        tk.Label(
            banner_inner,
            text=f"ชั้น {profile['student_class']}  ·  แผน{profile['study_plan']}  ·  รหัสนักเรียน {profile['student_code']}",
            font=(self.font_family, 9),
            bg=COLORS["card_bg"],
            fg=COLORS["text_muted"],
        ).pack(anchor="w", pady=(4, 0))

        stats = tk.Frame(content, bg=COLORS["bg"])
        stats.pack(fill="x", pady=(0, 20))

        total = profile["total_credits"] or 0
        earned = profile["credits_earned"] or 0
        percent = round(earned / total * 100) if total else 0

        self.stat_card(stats, "หน่วยกิตรวม", f"{total} นก.", "ของหลักสูตรทั้งหมด", COLORS["accent"])
        self.stat_card(stats, "เรียนแล้ว", f"{earned} นก.", f"สำเร็จแล้ว {percent}%", COLORS["success"])
        self.stat_card(stats, "หน่วยกิตคงเหลือ", f"{total - earned} นก.", "จนจบหลักสูตร", COLORS["warning"])
        self.stat_card(stats, "GPAX สะสม", f"{profile['gpax']:.2f}", f"เป้าหมาย {profile['target_gpax']:.2f}", COLORS["accent"])

        body = tk.Frame(content, bg=COLORS["bg"])
        body.pack(fill="both", expand=True)

        left_outer, left_inner = self.card(body, padding=18)
        left_outer.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(
            left_inner,
            text="ความก้าวหน้าตามกลุ่มสาระ",
            font=(self.font_family, 11, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w", pady=(0, 12))

        for row in self.db.all("SELECT * FROM progress"):
            row_frame = tk.Frame(left_inner, bg=COLORS["card_bg"])
            row_frame.pack(fill="x", pady=2)

            tk.Label(
                row_frame,
                text=row["subject"],
                font=(self.font_family, 9),
                bg=COLORS["card_bg"],
                fg=COLORS["text_dark"],
            ).pack(side="left")

            tk.Label(
                row_frame,
                text=f"{row['percentage']}%",
                font=(self.font_family, 9, "bold"),
                bg=COLORS["card_bg"],
                fg=COLORS["accent"],
            ).pack(side="right")

            self.draw_progress_bar(left_inner, row["percentage"])

        right_outer, right_inner = self.card(body, padding=18)
        right_outer.pack(side="left", fill="both", expand=True, padx=(10, 0))

        task_header = tk.Frame(right_inner, bg=COLORS["card_bg"])
        task_header.pack(fill="x", pady=(0, 12))

        tk.Label(
            task_header,
            text="งานค้างและแจ้งเตือน",
            font=(self.font_family, 11, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(side="left")

        ModernButton(
            task_header,
            text="＋ เพิ่มงานค้าง",
            command=self.add_task_dialog,
            font_tuple=(self.font_family, 8, "bold")
        ).pack(side="right")

        tasks = self.db.all("SELECT * FROM tasks ORDER BY id DESC")

        for task in tasks:
            task_card = tk.Frame(right_inner, bg=COLORS["bg"], padx=12, pady=10)
            task_card.pack(fill="x", pady=4)

            top_row = tk.Frame(task_card, bg=COLORS["bg"])
            top_row.pack(fill="x")

            tk.Label(
                top_row,
                text=task["title"],
                font=(self.font_family, 9, "bold"),
                bg=COLORS["bg"],
                fg=COLORS["text_dark"],
            ).pack(side="left")

            badge = tk.Label(
                top_row,
                text=task["status"],
                font=(self.font_family, 8, "bold"),
                bg=task["status_color"] or COLORS["accent"],
                fg="white",
                padx=6,
                pady=1,
            )
            badge.pack(side="right")

            tk.Label(
                task_card,
                text=task["detail"],
                font=(self.font_family, 8),
                bg=COLORS["bg"],
                fg=COLORS["text_muted"],
            ).pack(anchor="w", pady=(4, 0))

    def add_task_dialog(self):
        window = tk.Toplevel(self)
        window.title("เพิ่มงานค้างใหม่")
        window.geometry("420x360")
        window.resizable(False, False)
        window.configure(bg=COLORS["card_bg"])

        tk.Label(
            window,
            text="เพิ่มรายการงานค้าง",
            font=(self.font_family, 13, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w", padx=24, pady=(20, 10))

        # Title
        tk.Label(window, text="ชื่องาน", bg=COLORS["card_bg"], fg=COLORS["text_muted"], font=(self.font_family, 9)).pack(anchor="w", padx=24)
        entry_title = tk.Entry(window, font=(self.font_family, 10), bd=1, relief="solid")
        entry_title.pack(fill="x", padx=24, pady=(2, 10), ipady=5)

        # Detail
        tk.Label(window, text="รายละเอียด / กำหนดส่ง", bg=COLORS["card_bg"], fg=COLORS["text_muted"], font=(self.font_family, 9)).pack(anchor="w", padx=24)
        entry_detail = tk.Entry(window, font=(self.font_family, 10), bd=1, relief="solid")
        entry_detail.pack(fill="x", padx=24, pady=(2, 10), ipady=5)

        # Status Dropdown
        tk.Label(window, text="ระดับความสำคัญ", bg=COLORS["card_bg"], fg=COLORS["text_muted"], font=(self.font_family, 9)).pack(anchor="w", padx=24)
        status_var = tk.StringVar(value="ด่วน")
        status_combo = ttk.Combobox(window, textvariable=status_var, values=["ด่วน", "กำลังทำ", "รอดำเนินการ", "เสร็จแล้ว"], state="readonly")
        status_combo.pack(fill="x", padx=24, pady=(2, 16))

        def save_task():
            title = entry_title.get().strip()
            detail = entry_detail.get().strip()
            status = status_var.get()

            if not title:
                messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่องาน")
                return

            color_map = {
                "ด่วน": COLORS["warning"],
                "กำลังทำ": COLORS["accent"],
                "รอดำเนินการ": COLORS["text_muted"],
                "เสร็จแล้ว": COLORS["success"]
            }

            self.db.conn.execute("""
                INSERT INTO tasks (title, detail, status, status_color)
                VALUES (?, ?, ?, ?)
            """, (title, detail, status, color_map.get(status, COLORS["accent"])))
            self.db.commit()

            window.destroy()
            self.show_page("home")

        ModernButton(
            window, text="บันทึกงานค้าง", command=save_task, font_tuple=(self.font_family, 10, "bold")
        ).pack(fill="x", padx=24, pady=10)

    # ---------------- PLAN ----------------

    def plan_page(self):
        self.header("แผนการเรียน")
        content = self.content()
        profile = self.db.one("SELECT * FROM profile WHERE id=1")

        tk.Label(
            content,
            text=f"โครงสร้างแผนการเรียน: แผน{profile['study_plan']}",
            font=(self.font_family, 12, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w", pady=(0, 12))

        self.create_table(
            content,
            self.db.all("SELECT * FROM courses ORDER BY id"),
            [
                ("code", "รหัสวิชา"),
                ("name", "ชื่อวิชา"),
                ("category", "กลุ่มสาระ"),
                ("credits", "หน่วยกิต"),
                ("status", "สถานะ"),
            ],
        )

    # ---------------- COURSES ----------------

    def courses_page(self):
        self.header("รายวิชา")
        content = self.content()

        tk.Label(
            content,
            text="รายวิชาทั้งหมดในระบบ",
            font=(self.font_family, 12, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w", pady=(0, 12))

        self.create_table(
            content,
            self.db.all("SELECT * FROM courses"),
            [
                ("code", "รหัส"),
                ("name", "ชื่อรายวิชา"),
                ("category", "กลุ่มสาระ"),
                ("credits", "หน่วยกิต"),
                ("status", "สถานะ"),
            ],
        )

    # ---------------- GRADES ----------------

    def grades_page(self):
        self.header("ผลการเรียน")
        content = self.content()
        profile = self.db.one("SELECT * FROM profile WHERE id=1")

        stats = tk.Frame(content, bg=COLORS["bg"])
        stats.pack(fill="x", pady=(0, 16))

        self.stat_card(stats, "GPAX ปัจจุบัน", f"{profile['gpax']:.2f}")
        self.stat_card(stats, "เป้าหมาย", f"{profile['target_gpax']:.2f}")
        self.stat_card(stats, "หน่วยกิตรวม", f"{profile['credits_earned']}/{profile['total_credits']}")

        self.create_table(
            content,
            self.db.all("SELECT * FROM grades"),
            [
                ("term", "ภาคเรียน"),
                ("code", "รหัส"),
                ("name", "วิชา"),
                ("category", "กลุ่ม"),
                ("credits", "หน่วยกิต"),
                ("grade", "เกรด"),
                ("status", "สถานะ"),
            ],
        )

    # ---------------- PORTFOLIO ----------------

    def portfolio_page(self):
        self.header("ช่วยทำ Portfolio")
        content = self.content()

        toolbar = tk.Frame(content, bg=COLORS["bg"])
        toolbar.pack(fill="x", pady=(0, 14))

        tk.Label(
            toolbar,
            text="รายการผลงานสะสม",
            font=(self.font_family, 12, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text_dark"],
        ).pack(side="left")

        ModernButton(
            toolbar,
            text="＋ เพิ่มผลงานใหม่",
            command=self.add_portfolio,
            font_tuple=(self.font_family, 10, "bold")
        ).pack(side="right")

        self.create_table(
            content,
            self.db.all("SELECT * FROM portfolio"),
            [
                ("title", "ผลงาน"),
                ("category", "หมวดหมู่"),
                ("level", "ระดับ"),
                ("period", "ช่วงเวลา"),
                ("description", "รายละเอียด"),
            ],
        )

    def add_portfolio(self):
        window = tk.Toplevel(self)
        window.title("เพิ่มผลงาน")
        window.geometry("480x480")
        window.resizable(False, False)
        window.configure(bg=COLORS["card_bg"])

        entries = {}
        fields = [
            ("ชื่อผลงาน", "title"),
            ("หมวดหมู่", "category"),
            ("ระดับ", "level"),
            ("ช่วงเวลา", "period"),
            ("รายละเอียด", "description"),
        ]

        tk.Label(
            window,
            text="เพิ่มรายการ Portfolio",
            font=(self.font_family, 14, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w", padx=24, pady=(20, 10))

        for label, key in fields:
            frame = tk.Frame(window, bg=COLORS["card_bg"])
            frame.pack(fill="x", padx=24, pady=6)

            tk.Label(
                frame,
                text=label,
                bg=COLORS["card_bg"],
                fg=COLORS["text_muted"],
                font=(self.font_family, 9),
            ).pack(anchor="w", pady=(0, 2))

            entry = tk.Entry(frame, font=(self.font_family, 10), bd=1, relief="solid")
            entry.pack(fill="x", ipady=6)
            entries[key] = entry

        def save():
            values = [entries[key].get().strip() for _, key in fields]
            if not values[0]:
                messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่อผลงาน")
                return

            self.db.conn.execute("""
                INSERT INTO portfolio (title, category, level, period, description)
                VALUES (?, ?, ?, ?, ?)
            """, values)
            self.db.commit()

            window.destroy()
            self.show_page("portfolio")

        ModernButton(
            window, text="บันทึกข้อมูล", command=save, font_tuple=(self.font_family, 10, "bold")
        ).pack(fill="x", padx=24, pady=20)

    # ---------------- CAREERS ----------------

    def careers_page(self):
        self.header("แนะแนวอาชีพ")
        content = self.content()

        tk.Label(
            content,
            text="อาชีพที่เหมาะสมกับแผนการเรียนของคุณ",
            font=(self.font_family, 12, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w", pady=(0, 12))

        self.create_table(
            content,
            self.db.all("SELECT * FROM careers ORDER BY match_rate DESC"),
            [
                ("name", "อาชีพ"),
                ("faculty", "คณะ"),
                ("match_rate", "ความเหมาะสม %"),
                ("description", "รายละเอียด"),
                ("subjects", "วิชาแนะนำ"),
            ],
        )

    # ---------------- SETTINGS ----------------

    def settings_page(self):
        self.header("ตั้งค่า")
        content = self.content()
        profile = self.db.one("SELECT * FROM profile WHERE id=1")

        outer, inner = self.card(content, padding=24)
        outer.pack(fill="both", expand=True)

        tk.Label(
            inner,
            text="แก้ไขข้อมูลส่วนตัวและเป้าหมาย",
            font=(self.font_family, 12, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(anchor="w", pady=(0, 16))

        form = tk.Frame(inner, bg=COLORS["card_bg"])
        form.pack(fill="x")

        fields = [
            ("ชื่อ-นามสกุล", "student_name"),
            ("ระดับชั้น", "student_class"),
            ("แผนการเรียน", "study_plan"),
            ("รหัสนักเรียน", "student_code"),
            ("อาจารย์ที่ปรึกษา", "advisor_name"),
            ("มหาวิทยาลัยเป้าหมาย", "target_university"),
            ("GPAX เป้าหมาย", "target_gpax"),
            ("GPAX ปัจจุบัน", "gpax"),
            ("ชื่อโรงเรียน", "school_name"),
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            row = i // 2
            column = i % 2

            frame = tk.Frame(form, bg=COLORS["card_bg"])
            frame.grid(row=row, column=column, sticky="ew", padx=10, pady=8)
            form.columnconfigure(column, weight=1)

            tk.Label(
                frame,
                text=label,
                bg=COLORS["card_bg"],
                fg=COLORS["text_muted"],
                font=(self.font_family, 9),
            ).pack(anchor="w", pady=(0, 2))

            entry = tk.Entry(frame, font=(self.font_family, 10), bd=1, relief="solid")
            entry.pack(fill="x", ipady=6)

            val = profile[key]
            entry.insert(0, "" if val is None else str(val))
            entries[key] = entry

        def save():
            try:
                target_gpax = float(entries["target_gpax"].get())
                gpax = float(entries["gpax"].get())
            except ValueError:
                messagebox.showerror("ข้อมูลไม่ถูกต้อง", "GPAX ต้องเป็นตัวเลข เช่น 3.50")
                return

            self.db.conn.execute("""
                UPDATE profile
                SET
                    student_name=?, student_class=?, study_plan=?,
                    student_code=?, advisor_name=?, target_university=?,
                    target_gpax=?, gpax=?, school_name=?
                WHERE id=1
            """, (
                entries["student_name"].get().strip(),
                entries["student_class"].get().strip(),
                entries["study_plan"].get().strip(),
                entries["student_code"].get().strip(),
                entries["advisor_name"].get().strip(),
                entries["target_university"].get().strip(),
                target_gpax,
                gpax,
                entries["school_name"].get().strip(),
            ))

            self.db.commit()
            self.create_sidebar()
            messagebox.showinfo("สำเร็จ", "บันทึกข้อมูลเรียบร้อยแล้ว")
            self.show_page("settings")

        ModernButton(
            inner, text="บันทึกการเปลี่ยนแปลง", command=save, font_tuple=(self.font_family, 10, "bold")
        ).pack(anchor="w", pady=(20, 0))


if __name__ == "__main__":
    app = AcademicGuidance()
    app.mainloop()
