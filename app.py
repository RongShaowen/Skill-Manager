"""Main application window.

V1.4.1 — marketplace removed, security + dedup preserved.
Layout restored to V1.2 style (no marketplace panel).
"""

__version__ = "1.4.1"

import os
import threading

import customtkinter as ctk

from ui.theme import COLORS, FONT_HEADING, FONT_BODY, WINDOW_W, WINDOW_H
from ui.sidebar import Sidebar
from ui.skill_detail import DetailPanel
from ui.components import ScrollableCardGrid
from ui.download_dialog import DownloadDialog
from utils.i18n import t
from core.scanner import scan_all_skills, SkillInfo
from core.manager import (
    delete_skill,
    open_skill_dir,
    sync_skill,
    get_sync_targets,
)


class App(ctk.CTk):
    """Skill Manager main window."""

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title(t("app_title"))
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.minsize(900, 550)
        self.configure(fg_color=COLORS["bg_dark"])

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - WINDOW_W) // 2
        y = (self.winfo_screenheight() - WINDOW_H) // 2
        self.geometry(f"+{x}+{y}")

        self._all_skills: list[SkillInfo] = []
        self._current_filter = "all"
        self._debounce_id = None

        self._build_ui()
        self._load_skills()

    # ── UI construction ──────────────────────────────────────
    def _build_ui(self):
        # Main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar ───────────────────────────────────────────
        self._sidebar = Sidebar(self, on_filter=self._on_filter)
        self._sidebar.grid(row=0, column=0, sticky="nsw")

        # ── Center area ───────────────────────────────────────
        center = ctk.CTkFrame(self, fg_color=COLORS["bg_panel"], corner_radius=0)
        center.grid(row=0, column=1, sticky="nsew")
        center.grid_columnconfigure(0, weight=1)
        center.grid_rowconfigure(1, weight=1)

        # Top bar
        topbar = ctk.CTkFrame(center, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 0))
        topbar.grid_columnconfigure(0, weight=1)

        # Search
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", self._on_search)
        self._search_entry = ctk.CTkEntry(
            topbar, textvariable=self._search_var,
            placeholder_text=t("search_placeholder"),
            font=FONT_BODY, fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"],
            border_color=COLORS["border"], border_width=1,
            height=36, corner_radius=6, width=300
        )
        self._search_entry.grid(row=0, column=0, sticky="w")

        # Action button — download only (marketplace removed)
        btn_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e")

        self._download_btn = ctk.CTkButton(
            btn_frame, text=f"  {t('btn_download')}", font=FONT_BODY,
            fg_color=COLORS["accent_green"], hover_color="#059669",
            text_color="#ffffff", height=34, corner_radius=6,
            command=self._open_download
        )
        self._download_btn.pack(side="right")

        # Skill count label
        self._count_label = ctk.CTkLabel(
            topbar, text="", font=FONT_BODY,
            text_color=COLORS["text_dim"]
        )
        self._count_label.grid(row=0, column=2, padx=(12, 0), sticky="e")

        # ── Skill grid (scrollable) ───────────────────────────
        self._card_grid = ScrollableCardGrid(center, on_select=self._on_skill_select)
        self._card_grid.grid(row=1, column=0, sticky="nsew", padx=8, pady=(8, 0))

        # ── Detail panel ──────────────────────────────────────
        self._detail = DetailPanel(
            self, on_delete=self._on_delete, on_open_dir=self._on_open_dir,
            on_sync=self._on_sync
        )
        self._detail.grid(row=0, column=2, sticky="nsew")

    # ── Skill data ──────────────────────────────────────────
    def _load_skills(self):
        """Load all skills in a background thread."""
        def _scan():
            skills = scan_all_skills()
            self.after(0, lambda: self._set_skills(skills))
        threading.Thread(target=_scan, daemon=True).start()

    def _set_skills(self, skills: list[SkillInfo]):
        self._all_skills = skills
        counts = {}
        cat_counts = {}
        for s in skills:
            counts[s.source] = counts.get(s.source, 0) + 1
            cat_counts[s.category] = cat_counts.get(s.category, 0) + 1
        self._sidebar.update_stats(counts, cat_counts)
        self._refresh_view()

    def _refresh_view(self):
        """Rebuild the card grid based on current filter and search."""
        skills = self._all_skills
        if self._current_filter != "all":
            skills = [s for s in skills if s.category == self._current_filter]

        query = self._search_var.get().strip().lower()
        if query:
            skills = [
                s for s in skills
                if query in s.name.lower()
                or query in s.description.lower()
                or query in s.cn_description.lower()
            ]

        self._count_label.configure(text=f"{len(skills)} / {len(self._all_skills)}")
        self._card_grid.populate(skills)

    # ── Event handlers ──────────────────────────────────────
    def _on_filter(self, source: str):
        self._current_filter = source
        self._refresh_view()

    def _on_search(self, *_):
        """Debounced search: wait 300 ms after last keystroke."""
        if self._debounce_id is not None:
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(300, self._refresh_view)

    def _on_skill_select(self, skill: SkillInfo):
        self._detail.show_skill(skill)

    def _on_delete(self, skill: SkillInfo):
        from tkinter import messagebox
        msg = t("delete_msg", name=skill.name, path=skill.path)
        if messagebox.askyesno(t("delete_confirm"), msg):
            if delete_skill(skill.path):
                self._all_skills = [s for s in self._all_skills if s.path != skill.path]
                self._detail.show_empty()
                # Update stats
                counts = {}
                cat_counts = {}
                for s in self._all_skills:
                    counts[s.source] = counts.get(s.source, 0) + 1
                    cat_counts[s.category] = cat_counts.get(s.category, 0) + 1
                self._sidebar.update_stats(counts, cat_counts)
                self._refresh_view()
            else:
                messagebox.showerror(t("delete_fail"), t("delete_fail"))

    def _on_open_dir(self, path: str):
        open_skill_dir(path)

    def _on_sync(self, skill: SkillInfo):
        from tkinter import messagebox
        targets = get_sync_targets(skill.path)
        if not targets:
            return
        target_names = ", ".join(targets)
        msg = t("sync_msg", name=skill.name) + f"\n\n{target_names}"
        if messagebox.askyesno(t("sync_title"), msg):
            try:
                for target in targets:
                    sync_skill(skill.path, target)
                messagebox.showinfo(t("sync_success"), t("sync_success"))
            except Exception as e:
                messagebox.showerror(t("sync_fail"), str(e))

    def _open_download(self):
        DownloadDialog(self, on_complete=self._on_download_complete)

    def _on_download_complete(self, path: str):
        self._load_skills()
