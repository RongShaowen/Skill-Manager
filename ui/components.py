"""Reusable customtkinter widgets with sci-fi styling."""

import customtkinter as ctk
from ui.theme import (
    COLORS, FONT_BODY, FONT_SMALL, FONT_CODE, FONT_STAT_NUM,
    FONT_CARD_NAME, FONT_CARD_DESC, FONT_BADGE, CATEGORY_COLORS,
)


class GlowFrame(ctk.CTkFrame):
    """Frame with a subtle glowing border."""

    def __init__(self, master, glow_color=None, **kw):
        kw.setdefault("fg_color", COLORS["bg_card"])
        kw.setdefault("corner_radius", 8)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", glow_color or COLORS["border"])
        super().__init__(master, **kw)


def _darken(hex_color: str, factor: float = 0.25) -> str:
    """Blend a hex color toward black for badge backgrounds."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


class SourceBadge(ctk.CTkLabel):
    """Small colored badge showing the skill source."""

    def __init__(self, master, source: str, **kw):
        from ui.theme import SOURCE_COLORS
        color = SOURCE_COLORS.get(source, COLORS["text_dim"])
        kw.setdefault("text", source.upper())
        kw.setdefault("text_color", color)
        kw.setdefault("font", FONT_BADGE)
        kw.setdefault("fg_color", _darken(color, 0.25))
        kw.setdefault("corner_radius", 4)
        kw.setdefault("height", 22)
        kw.setdefault("padx", 6)
        super().__init__(master, **kw)


class CategoryBadge(ctk.CTkLabel):
    """Badge showing skill category (cross_platform/native/installed)."""

    def __init__(self, master, category: str, **kw):
        labels = {"cross_platform": "跨平台", "native": "平台专属", "installed": "用户安装"}
        color = CATEGORY_COLORS.get(category, COLORS["text_dim"])
        text = labels.get(category, category)
        kw.setdefault("text", text)
        kw.setdefault("text_color", color)
        kw.setdefault("font", FONT_BADGE)
        kw.setdefault("fg_color", _darken(color, 0.25))
        kw.setdefault("corner_radius", 4)
        kw.setdefault("height", 22)
        kw.setdefault("padx", 6)
        super().__init__(master, **kw)


class SkillCard(ctk.CTkFrame):
    """Clickable card representing a single skill."""

    def __init__(self, master, skill_info, on_click=None, **kw):
        kw.setdefault("fg_color", COLORS["bg_card"])
        kw.setdefault("corner_radius", 8)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", COLORS["border"])
        kw.setdefault("cursor", "hand2")
        super().__init__(master, **kw)
        self.skill = skill_info
        self._on_click = on_click
        self._hover = False

        self.grid_columnconfigure(0, weight=1)

        # Source badge + category badge
        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.grid(row=0, column=0, padx=12, pady=(10, 0), sticky="ew")
        top_row.grid_columnconfigure(0, weight=1)

        SourceBadge(top_row, skill_info.source).grid(row=0, column=0, sticky="w")
        CategoryBadge(top_row, skill_info.category).grid(row=0, column=1, padx=(6, 0), sticky="e")

        # Name
        name_label = ctk.CTkLabel(
            self, text=skill_info.name, font=FONT_CARD_NAME,
            text_color=COLORS["text_primary"], anchor="w", wraplength=220
        )
        name_label.grid(row=1, column=0, padx=12, pady=(6, 0), sticky="w")

        # Chinese description (primary) with English fallback
        cn_desc = skill_info.cn_description
        en_desc = skill_info.description
        if cn_desc and cn_desc != en_desc:
            display_desc = cn_desc
        else:
            display_desc = en_desc
        if len(display_desc) > 80:
            display_desc = display_desc[:77] + "..."
        desc_label = ctk.CTkLabel(
            self, text=display_desc, font=FONT_CARD_DESC,
            text_color=COLORS["text_secondary"], anchor="w",
            wraplength=220, justify="left"
        )
        desc_label.grid(row=2, column=0, padx=12, pady=(4, 10), sticky="w")

        # Bind click
        for widget in [self, name_label, desc_label]:
            widget.bind("<Button-1>", self._clicked)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _clicked(self, event=None):
        if self._on_click:
            self._on_click(self.skill)

    def _on_enter(self, event=None):
        self.configure(fg_color=COLORS["bg_card_hover"], border_color=COLORS["glow"])
        self._hover = True

    def _on_leave(self, event=None):
        if not self._selected:
            self.configure(fg_color=COLORS["bg_card"], border_color=COLORS["border"])
        self._hover = False

    _selected = False

    def set_selected(self, selected: bool):
        self._selected = selected
        if selected:
            self.configure(fg_color=COLORS["bg_card_hover"], border_color=COLORS["accent_blue"])
        else:
            self.configure(fg_color=COLORS["bg_card"], border_color=COLORS["border"])


class ScrollableCardGrid(ctk.CTkScrollableFrame):
    """Scrollable grid of SkillCards with performance optimization."""

    def __init__(self, master, on_select=None, **kw):
        kw.setdefault("fg_color", COLORS["bg_panel"])
        kw.setdefault("scrollbar_button_color", COLORS["border"])
        kw.setdefault("scrollbar_button_hover_color", COLORS["accent_blue"])
        kw.setdefault("corner_radius", 0)
        super().__init__(master, **kw)
        self._cards: list[SkillCard] = []
        self._on_select = on_select
        self._selected_card = None
        self.grid_columnconfigure(0, weight=1)
        self._last_skills: list = []

    def populate(self, skills: list):
        """Clear and populate with SkillInfo list. Skips if unchanged."""
        # Performance: skip if same skill list
        if skills is self._last_skills:
            return
        self._last_skills = skills

        # Batch destroy
        for card in self._cards:
            card.destroy()
        self._cards.clear()
        self._selected_card = None

        cols = max(1, (self.winfo_width() - 20) // 250) if self.winfo_width() > 250 else 3

        # Pre-create all cards in batch
        new_cards = []
        for i, skill in enumerate(skills):
            card = SkillCard(self, skill, on_click=self._card_clicked)
            row, col = divmod(i, cols)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
            new_cards.append(card)
        self._cards = new_cards

    def _card_clicked(self, skill):
        if self._selected_card:
            self._selected_card.set_selected(False)
        for card in self._cards:
            if card.skill is skill:
                card.set_selected(True)
                self._selected_card = card
                break
        if self._on_select:
            self._on_select(skill)
