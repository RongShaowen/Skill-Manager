"""Download dialog — input URL and download a skill.

V1.4.1 — kept V1.2 style, kept cancelable download from V1.3.
"""

import threading

import customtkinter as ctk
from ui.theme import COLORS, FONT_HEADING, FONT_BODY, FONT_SMALL
from utils.i18n import t


class DownloadDialog(ctk.CTkToplevel):
    """Modal dialog for downloading a skill from URL."""

    def __init__(self, parent, on_complete=None, **kw):
        super().__init__(parent, **kw)
        self._on_complete = on_complete
        self._cancel_event = threading.Event()

        self.title(t("download_title"))
        self.geometry("480x220")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_dark"])
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width() // 2 - 240
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 110
        self.geometry(f"+{px}+{py}")

        self._build_ui()

    def _build_ui(self):
        pad = dict(padx=20)

        ctk.CTkLabel(
            self, text=t("download_title"), font=FONT_HEADING,
            text_color=COLORS["accent_green"]
        ).pack(anchor="w", pady=(16, 4), **pad)

        ctk.CTkLabel(
            self, text=t("download_hint"), font=FONT_SMALL,
            text_color=COLORS["text_dim"]
        ).pack(anchor="w", **pad)

        # URL input
        self._url_var = ctk.StringVar()
        self._url_entry = ctk.CTkEntry(
            self, textvariable=self._url_var,
            placeholder_text="https://github.com/owner/repo",
            font=FONT_BODY, fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"],
            border_color=COLORS["border"], border_width=1,
            height=36, corner_radius=6
        )
        self._url_entry.pack(fill="x", pady=(8, 0), **pad)

        # Status label
        self._status = ctk.CTkLabel(
            self, text="", font=FONT_SMALL,
            text_color=COLORS["text_secondary"]
        )
        self._status.pack(anchor="w", pady=(8, 0), **pad)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(12, 16), **pad)

        self._cancel_btn = ctk.CTkButton(
            btn_frame, text=t("btn_cancel"), font=FONT_BODY,
            fg_color=COLORS["bg_input"], hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_primary"],
            height=34, width=90, corner_radius=6,
            command=self._on_cancel
        )
        self._cancel_btn.pack(side="right")

        self._download_btn = ctk.CTkButton(
            btn_frame, text=t("btn_download"), font=FONT_BODY,
            fg_color=COLORS["accent_green"], hover_color="#059669",
            text_color="#ffffff", height=34, width=120, corner_radius=6,
            command=self._on_download
        )
        self._download_btn.pack(side="right", padx=(0, 8))

    def _on_download(self):
        url = self._url_var.get().strip()
        if not url:
            self._status.configure(text=t("download_empty"), text_color=COLORS["accent_red"])
            return
        if not url.startswith("https://"):
            self._status.configure(text=t("download_https_only"), text_color=COLORS["accent_red"])
            return

        self._download_btn.configure(state="disabled")
        self._cancel_btn.configure(state="normal")
        self._cancel_event.clear()
        self._status.configure(text=t("download_progress"), text_color=COLORS["text_secondary"])

        def _run():
            from core.downloader import download_skill
            try:
                result = download_skill(url, progress_callback=self._progress)
                self.after(0, lambda: self._done(result))
            except Exception as e:
                if self._cancel_event.is_set():
                    self.after(0, lambda: self._cancelled())
                else:
                    self.after(0, lambda: self._error(str(e)))

        threading.Thread(target=_run, daemon=True).start()

    def _progress(self, msg: str):
        if not self._cancel_event.is_set():
            self.after(0, lambda: self._status.configure(text=msg))

    def _done(self, path: str):
        self._status.configure(text=t("download_success"), text_color=COLORS["accent_green"])
        self._download_btn.configure(state="normal")
        if self._on_complete:
            self._on_complete(path)
        self.after(1500, self.destroy)

    def _error(self, msg: str):
        self._status.configure(text=msg, text_color=COLORS["accent_red"])
        self._download_btn.configure(state="normal")

    def _cancelled(self):
        self._status.configure(text=t("download_cancelled"), text_color=COLORS["text_dim"])
        self._download_btn.configure(state="normal")

    def _on_cancel(self):
        self._cancel_event.set()
