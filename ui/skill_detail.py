"""Detail panel showing skill information."""

import os
import customtkinter as ctk
from ui.theme import COLORS, FONT_HEADING, FONT_BODY, FONT_SMALL, FONT_CODE, SOURCE_COLORS
from utils.i18n import t


class DetailPanel(ctk.CTkFrame):
    def __init__(self, master, on_delete=None, on_open_dir=None, on_sync=None, **kw):
        kw["width"] = 340
        kw["fg_color"] = COLORS["bg_dark"]
        kw["corner_radius"] = 0
        kw["border_width"] = 0
        super().__init__(master, **kw)
        self.pack_propagate(False)
        self._on_delete = on_delete
        self._on_open_dir = on_open_dir
        self._on_sync = on_sync
        self._skill = None

        # Title
        self._title = ctk.CTkLabel(
            self, text="技能详情", font=FONT_HEADING,
            text_color=COLORS["text_primary"], anchor="w"
        )
        self._title.pack(fill="x", padx=20, pady=(20, 4))

        ctk.CTkFrame(self, fg_color=COLORS["border"], height=1).pack(
            fill="x", padx=20, pady=(0, 12)
        )

        # Scrollable content
        self._content = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent_blue"]
        )
        self._content.pack(fill="both", expand=True, padx=0)

        # Info labels
        self._info_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        self._info_frame.pack(fill="x", padx=20)

        self._name_label = self._make_label("name", "")
        self._source_label = self._make_label("source", "")
        self._path_label = self._make_label("path", "", font=FONT_CODE)
        self._version_label = self._make_label("version", "")
        self._size_label = self._make_label("size", "")

        # Description
        ctk.CTkLabel(
            self._info_frame, text=t("detail_desc"),
            font=FONT_SMALL, text_color=COLORS["text_dim"], anchor="w"
        ).grid(row=5, column=0, sticky="w", pady=(8, 0))
        self._desc_text = ctk.CTkTextbox(
            self._info_frame, font=FONT_SMALL, fg_color=COLORS["bg_panel"],
            text_color=COLORS["text_secondary"], height=80,
            corner_radius=6, border_width=1, border_color=COLORS["border"],
            activate_scrollbars=True
        )
        self._desc_text.grid(row=6, column=0, sticky="ew", pady=(4, 0))

        # Files list
        ctk.CTkLabel(
            self._info_frame, text=t("detail_files"),
            font=FONT_SMALL, text_color=COLORS["text_dim"], anchor="w"
        ).grid(row=7, column=0, sticky="w", pady=(12, 0))
        self._files_text = ctk.CTkTextbox(
            self._info_frame, font=FONT_CODE, fg_color=COLORS["bg_panel"],
            text_color=COLORS["accent_cyan"], height=100,
            corner_radius=6, border_width=1, border_color=COLORS["border"],
            activate_scrollbars=True
        )
        self._files_text.grid(row=8, column=0, sticky="ew", pady=(4, 0))

        self._info_frame.grid_columnconfigure(0, weight=1)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(12, 16))

        self._open_btn = ctk.CTkButton(
            btn_frame, text=f"  {t('btn_open_dir')}", font=FONT_BODY,
            fg_color=COLORS["accent_blue"], hover_color="#2563eb",
            height=36, corner_radius=6,
            command=self._open_dir
        )
        self._open_btn.pack(fill="x", pady=(0, 6))

        self._delete_btn = ctk.CTkButton(
            btn_frame, text=f"  {t('btn_delete')}", font=FONT_BODY,
            fg_color=COLORS["accent_red"], hover_color="#dc2626",
            height=36, corner_radius=6,
            command=self._delete
        )
        self._delete_btn.pack(fill="x")

        # Sync button
        self._sync_btn = ctk.CTkButton(
            btn_frame, text=f"  {t('btn_sync')}", font=FONT_BODY,
            fg_color=COLORS["accent_purple"], hover_color="#7c3aed",
            height=36, corner_radius=6,
            command=self._sync
        )

        # Readonly notice
        self._readonly_label = ctk.CTkLabel(
            btn_frame, text=t("detail_readonly"),
            font=FONT_SMALL, text_color=COLORS["accent_gold"],
            wraplength=300
        )

        self.show_empty()

    def _make_label(self, key: str, value: str, font=FONT_BODY) -> ctk.CTkLabel:
        row = len(self._info_frame.winfo_children()) // 2
        ctk.CTkLabel(
            self._info_frame, text=t(f"detail_{key}"),
            font=FONT_SMALL, text_color=COLORS["text_dim"], anchor="w"
        ).grid(row=row * 2, column=0, sticky="w", pady=(8, 0))
        label = ctk.CTkLabel(
            self._info_frame, text=value, font=font,
            text_color=COLORS["text_primary"], anchor="w", wraplength=300
        )
        label.grid(row=row * 2 + 1, column=0, sticky="w")
        return label

    def show_skill(self, skill):
        """Display details for a SkillInfo."""
        self._skill = skill
        self._name_label.configure(text=skill.name)
        color = SOURCE_COLORS.get(skill.source, COLORS["text_dim"])
        self._source_label.configure(text=skill.source.upper(), text_color=color)
        self._path_label.configure(text=skill.path)
        self._version_label.configure(text=skill.version)
        self._size_label.configure(text=skill.size)

        # Show Chinese description first, English as supplement
        cn = skill.cn_description
        en = skill.description
        if cn and cn != en:
            display = f"【中文】{cn}\n\n【English】{en}"
        else:
            display = en
        self._desc_text.configure(state="normal")
        self._desc_text.delete("1.0", "end")
        self._desc_text.insert("1.0", display)
        self._desc_text.configure(state="disabled")

        self._files_text.configure(state="normal")
        self._files_text.delete("1.0", "end")
        self._files_text.insert("1.0", "\n".join(skill.files))
        self._files_text.configure(state="disabled")

        if skill.is_readonly:
            self._delete_btn.pack_forget()
            self._sync_btn.pack_forget()
            self._readonly_label.pack(fill="x")
        else:
            self._readonly_label.pack_forget()
            self._delete_btn.pack(fill="x")
            # Show sync only if there are targets
            from core.manager import get_sync_targets
            targets = get_sync_targets(skill.path)
            if targets:
                self._sync_btn.pack(fill="x", pady=(6, 0))
            else:
                self._sync_btn.pack_forget()

    def show_empty(self):
        """Show placeholder when no skill is selected."""
        self._skill = None
        self._name_label.configure(text="-")
        self._source_label.configure(text="-", text_color=COLORS["text_dim"])
        self._path_label.configure(text="-")
        self._version_label.configure(text="-")
        self._size_label.configure(text="-")

        self._desc_text.configure(state="normal")
        self._desc_text.delete("1.0", "end")
        self._desc_text.configure(state="disabled")

        self._files_text.configure(state="normal")
        self._files_text.delete("1.0", "end")
        self._files_text.configure(state="disabled")

        self._delete_btn.pack_forget()
        self._readonly_label.pack_forget()

    def _open_dir(self):
        if self._skill and self._on_open_dir:
            self._on_open_dir(self._skill.path)

    def _delete(self):
        if self._skill and self._on_delete:
            self._on_delete(self._skill)

    def _sync(self):
        if self._skill and self._on_sync:
            self._on_sync(self._skill)
