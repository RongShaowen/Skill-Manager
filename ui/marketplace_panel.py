"""Marketplace panel — browse and install community skills.

V1.4 changes:
  - Adapts to new fetch_marketplace() return signature (4-tuple with errors)
  - Shows detailed error messages when network fails
  - Displays which sources were tried and why they failed
"""

import threading
import customtkinter as ctk
from ui.theme import COLORS, FONT_HEADING, FONT_BODY, FONT_SMALL, FONT_CODE
from utils.i18n import t


class MarketplacePanel(ctk.CTkFrame):
    def __init__(self, master, on_install_complete=None, **kw):
        kw["fg_color"] = COLORS["bg_panel"]
        kw["corner_radius"] = 0
        super().__init__(master, **kw)
        self._on_install_complete = on_install_complete
        self._installed_names: set[str] = set()
        self._skills: list[dict] = []
        self._used_cache = False

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(
            header, text=f"  {t('btn_marketplace')}", font=FONT_HEADING,
            text_color=COLORS["accent_gold"]
        ).pack(side="left")

        self._refresh_btn = ctk.CTkButton(
            header, text=t("btn_refresh"), font=FONT_SMALL,
            fg_color=COLORS["accent_blue"], hover_color="#2563eb",
            height=28, width=70, corner_radius=4,
            command=self.load_marketplace
        )
        self._refresh_btn.pack(side="right")

        ctk.CTkFrame(self, fg_color=COLORS["border"], height=1).pack(fill="x", padx=20, pady=(0, 8))

        # Status label (loading / error / cache info)
        self._status_label = ctk.CTkLabel(
            self, text=t("marketplace_loading"), font=FONT_BODY,
            text_color=COLORS["text_secondary"]
        )
        self._status_label.pack(pady=20)

        # Error detail label (shows specific failure reasons)
        self._error_detail: ctk.CTkLabel | None = None

        # Scrollable list
        self._list_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent_blue"]
        )

    def load_marketplace(self, installed_names: set[str] = None):
        """Fetch marketplace index and display skills."""
        if installed_names is not None:
            self._installed_names = installed_names
        self._status_label.configure(text=t("marketplace_loading"), text_color=COLORS["text_secondary"])
        self._status_label.pack(pady=20)

        # Clear previous error details
        if self._error_detail:
            self._error_detail.destroy()
            self._error_detail = None

        self._list_frame.pack_forget()

        def _fetch():
            from core.marketplace import fetch_marketplace
            skills, cache_ts, used_cache, errors = fetch_marketplace()
            self._used_cache = used_cache
            self.after(0, lambda: self._render(skills, cache_ts, used_cache, errors))

        threading.Thread(target=_fetch, daemon=True).start()

    def _render(
        self,
        skills: list[dict],
        cache_ts: str | None,
        used_cache: bool,
        errors: list[str],
    ):
        self._skills = skills
        for w in self._list_frame.winfo_children():
            w.destroy()

        if not skills:
            # No skills at all — show error
            self._status_label.configure(
                text="技能市场加载失败", text_color=COLORS["accent_red"]
            )
            self._status_label.pack(pady=(20, 4))

            # Show detailed errors
            if errors:
                error_text = "\n".join(f"  • {e}" for e in errors)
                self._error_detail = ctk.CTkLabel(
                    self, text=error_text, font=FONT_SMALL,
                    text_color=COLORS["text_dim"], justify="left", anchor="w"
                )
                self._error_detail.pack(anchor="w", padx=20, pady=(0, 12))
            return

        # Skills loaded — show status if there were fallback errors
        if errors:
            # Show warning that we fell back
            warning_text = errors[-1] if errors else ""
            self._status_label.configure(
                text=f"⚠ {warning_text}", text_color=COLORS["accent_gold"]
            )
            self._status_label.pack(anchor="w", padx=20, pady=(0, 4))

            # Show full error details in smaller text
            error_text = "\n".join(f"  • {e}" for e in errors[:-1])
            if error_text:
                self._error_detail = ctk.CTkLabel(
                    self, text=error_text, font=FONT_SMALL,
                    text_color=COLORS["text_dim"], justify="left", anchor="w"
                )
                self._error_detail.pack(anchor="w", padx=20, pady=(0, 8))
        elif used_cache and cache_ts:
            self._status_label.configure(
                text=f"离线缓存（更新于 {cache_ts}）", text_color=COLORS["text_dim"]
            )
            self._status_label.pack(anchor="w", padx=20, pady=(0, 4))
        else:
            self._status_label.pack_forget()

        self._list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for i, skill in enumerate(skills):
            self._make_card(skill, i)

    def _make_card(self, skill: dict, idx: int):
        card = ctk.CTkFrame(
            self._list_frame, fg_color=COLORS["bg_card"],
            corner_radius=8, border_width=1, border_color=COLORS["border"]
        )
        card.pack(fill="x", padx=4, pady=4)
        card.grid_columnconfigure(0, weight=1)

        # Name + category
        top = ctk.CTkFrame(card, fg_color="transparent")
        top.grid(row=0, column=0, padx=12, pady=(10, 0), sticky="ew")
        top.grid_columnconfigure(0, weight=1)

        name = skill.get("name", "unknown")
        ctk.CTkLabel(
            top, text=name, font=("Segoe UI", 12, "bold"),
            text_color=COLORS["text_primary"], anchor="w"
        ).grid(row=0, column=0, sticky="w")

        cat = skill.get("category", "")
        if cat:
            ctk.CTkLabel(
                top, text=cat, font=("Cascadia Code", 8),
                text_color=COLORS["accent_purple"]
            ).grid(row=0, column=1, padx=(8, 0), sticky="e")

        # Description
        desc = skill.get("description", "")
        if len(desc) > 120:
            desc = desc[:117] + "..."
        ctk.CTkLabel(
            card, text=desc, font=FONT_SMALL,
            text_color=COLORS["text_secondary"], anchor="w",
            wraplength=500, justify="left"
        ).grid(row=1, column=0, padx=12, pady=(4, 0), sticky="w")

        # Author
        author = skill.get("author", "")
        if author:
            ctk.CTkLabel(
                card, text=f"by {author}", font=FONT_SMALL,
                text_color=COLORS["text_dim"], anchor="w"
            ).grid(row=2, column=0, padx=12, pady=(2, 0), sticky="w")

        # Install button
        is_installed = name in self._installed_names
        btn_text = t("marketplace_installed") if is_installed else t("marketplace_install")
        btn_color = COLORS["text_dim"] if is_installed else COLORS["accent_green"]

        btn = ctk.CTkButton(
            card, text=btn_text, font=FONT_SMALL,
            fg_color=btn_color, hover_color=btn_color,
            height=28, width=90, corner_radius=4,
            state="disabled" if is_installed else "normal",
            command=lambda n=name, u=skill.get("url", ""): self._install(n, u)
        )
        btn.grid(row=0, column=1, rowspan=2, padx=12, pady=10, sticky="e")

    def _install(self, name: str, url: str):
        if not url:
            return

        def _run():
            from core.downloader import download_skill
            from utils.logger import get_logger
            try:
                download_skill(url)
                self._installed_names.add(name)
                self.after(0, lambda: self._on_install_complete(name) if self._on_install_complete else None)
                self.after(0, self.load_marketplace)
            except ValueError as e:
                self.after(0, lambda: self._show_error(str(e)))
            except Exception as e:
                get_logger("marketplace_panel").error("Install failed: %s", e, exc_info=True)
                self.after(0, lambda: self._show_error(f"安装失败：{e}"))

        threading.Thread(target=_run, daemon=True).start()

    def _show_error(self, msg: str):
        if self._error_detail:
            self._error_detail.destroy()
        self._error_detail = ctk.CTkLabel(
            self, text=msg, font=FONT_SMALL,
            text_color=COLORS["accent_red"], justify="left", anchor="w"
        )
        self._error_detail.pack(anchor="w", padx=20, pady=(4, 8))
