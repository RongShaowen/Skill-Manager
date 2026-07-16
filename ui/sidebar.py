"""Left sidebar with navigation and statistics."""

import customtkinter as ctk
from ui.theme import COLORS, FONT_BODY, FONT_SMALL, FONT_STAT_NUM
from utils.i18n import t


class Sidebar(ctk.CTkFrame):
    """Left navigation sidebar with filters and stats."""

    def __init__(self, master, on_filter=None, **kw):
        kw.setdefault("fg_color", COLORS["bg_sidebar"])
        kw.setdefault("corner_radius", 0)
        kw.setdefault("width", 200)
        super().__init__(master, **kw)
        self._on_filter = on_filter

        # ── Title ─────────────────────────────────────────────
        ctk.CTkLabel(
            self, text="Skill Manager", font=("Segoe UI", 16, "bold"),
            text_color=COLORS["accent_blue"]
        ).pack(pady=(20, 2), padx=16, anchor="w")

        ctk.CTkLabel(
            self, text=f"v{self._get_version()}", font=FONT_SMALL,
            text_color=COLORS["text_dim"]
        ).pack(padx=16, anchor="w")

        # ── Divider ─────────────────────────────────────────
        ctk.CTkFrame(self, fg_color=COLORS["border"], height=1).pack(
            fill="x", padx=12, pady=(16, 8)
        )

        # ── Stats ───────────────────────────────────────────
        self._stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._stats_frame.pack(fill="x", padx=16, pady=(0, 8))

        self._total_label = ctk.CTkLabel(
            self._stats_frame, text="...", font=FONT_BODY,
            text_color=COLORS["text_primary"]
        )
        self._total_label.pack(anchor="w")

        # ── Divider ─────────────────────────────────────────
        ctk.CTkFrame(self, fg_color=COLORS["border"], height=1).pack(
            fill="x", padx=12, pady=(12, 8)
        )

        # ── Filter buttons ─────────────────────────────────
        self._filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._filter_frame.pack(fill="x", padx=12)
        self._filter_buttons: dict[str, ctk.CTkButton] = {}

        # "All" filter
        self._make_filter_btn("all", t("filter_all"))

        # Category filters will be added in update_stats()

        # ── Spacer ──────────────────────────────────────────
        ctk.CTkFrame(self, fg_color="transparent").pack(fill="both", expand=True)

        # ── Source legend ───────────────────────────────────
        self._legend_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._legend_frame.pack(fill="x", padx=16, pady=(0, 20))

        legend_title = ctk.CTkLabel(
            self._legend_frame, text=t("legend_title"), font=FONT_SMALL,
            text_color=COLORS["text_dim"]
        )
        legend_title.pack(anchor="w", pady=(0, 6))

    def _make_filter_btn(self, key: str, label: str):
        btn = ctk.CTkButton(
            self._filter_frame, text=label, font=FONT_BODY,
            fg_color=COLORS["bg_input"], hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_primary"],
            border_width=1, border_color=COLORS["border"],
            height=32, corner_radius=6, anchor="w",
            command=lambda k=key: self._activate(k)
        )
        btn.pack(fill="x", pady=1)
        self._filter_buttons[key] = btn
        return btn

    def _activate(self, key: str):
        for k, btn in self._filter_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=COLORS["accent_blue"],
                    text_color="#ffffff",
                    border_color=COLORS["accent_blue"]
                )
            else:
                btn.configure(
                    fg_color=COLORS["bg_input"],
                    text_color=COLORS["text_primary"],
                    border_color=COLORS["border"]
                )
        if self._on_filter:
            self._on_filter(key)

    def update_stats(self, counts: dict, cat_counts: dict):
        """Update statistics display and rebuild filters."""
        # Total
        total = sum(counts.values())
        self._total_label.configure(text=f"{t('total_skills')} {total}")

        # Rebuild category filter buttons
        for btn in self._filter_buttons.values():
            btn.destroy()
        self._filter_buttons.clear()

        self._make_filter_btn("all", t("filter_all"))
        for cat, cnt in cat_counts.items():
            self._make_filter_btn(cat, f"{cat} ({cnt})")

        # Rebuild legend
        for w in self._legend_frame.winfo_children():
            if w is not self._legend_frame.winfo_children()[0]:
                w.destroy()

        from ui.theme import SOURCE_COLORS
        for source, cnt in counts.items():
            row = ctk.CTkFrame(self._legend_frame, fg_color="transparent")
            row.pack(fill="x", pady=1)
            color = SOURCE_COLORS.get(source, COLORS["text_dim"])
            ctk.CTkLabel(
                row, text="●", font=FONT_SMALL, text_color=color
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=f" {source} ({cnt})", font=FONT_SMALL,
                text_color=COLORS["text_dim"]
            ).pack(side="left")

        # Activate "all" filter by default
        self._activate("all")

    @staticmethod
    def _get_version() -> str:
        try:
            from app import __version__
            return __version__
        except Exception:
            return "?"
