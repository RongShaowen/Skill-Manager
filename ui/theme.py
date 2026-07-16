"""Sci-fi theme: colors, fonts, and style constants."""

# ── Color Palette ──────────────────────────────────────────────
COLORS = {
    # Backgrounds
    "bg_dark":       "#0a0e17",
    "bg_panel":      "#111827",
    "bg_card":       "#1a2332",
    "bg_card_hover": "#1f2d40",
    "bg_input":      "#0d1520",
    # Accents
    "accent_blue":   "#3b82f6",
    "accent_cyan":   "#06b6d4",
    "accent_gold":   "#f59e0b",
    "accent_green":  "#10b981",
    "accent_red":    "#ef4444",
    "accent_purple": "#8b5cf6",
    "accent_pink":   "#ec4899",
    "accent_teal":   "#14b8a6",
    "accent_lime":   "#84cc16",
    "accent_orange": "#f97316",
    "accent_indigo": "#6366f1",
    "accent_rose":   "#f43f5e",
    # Text — brighter for readability
    "text_primary":   "#f1f5f9",
    "text_secondary": "#cbd5e1",
    "text_dim":       "#94a3b8",
    # Borders & effects
    "border":        "#1e3a5f",
    "border_light":  "#2d4a6f",
    "glow":          "#3b82f6",
    "glow_gold":     "#f59e0b",
    # Source badge colors
    "src_builtin":   "#f59e0b",
    "src_compose":   "#8b5cf6",
    "src_claude":    "#06b6d4",
    "src_agent":     "#10b981",
    "src_user":      "#3b82f6",
    "src_codex":     "#ec4899",
    "src_trae":      "#14b8a6",
    "src_cursor":    "#84cc16",
    "src_windsurf":  "#f97316",
    "src_continue":  "#6366f1",
    "src_aider":     "#f43f5e",
    "src_mcp":       "#64748b",
    "src_github_copilot": "#10b981",
    "src_cline":     "#06b6d4",
    "src_discovered":"#94a3b8",
}

SOURCE_COLORS = {
    "builtin":        COLORS["src_builtin"],
    "compose":        COLORS["src_compose"],
    "claude":         COLORS["src_claude"],
    "agent":          COLORS["src_agent"],
    "user":           COLORS["src_user"],
    "codex":          COLORS["src_codex"],
    "trae":           COLORS["src_trae"],
    "cursor":         COLORS["src_cursor"],
    "windsurf":       COLORS["src_windsurf"],
    "continue":       COLORS["src_continue"],
    "aider":          COLORS["src_aider"],
    "mcp":            COLORS["src_mcp"],
    "github_copilot": COLORS["src_github_copilot"],
    "cline":          COLORS["src_cline"],
    "discovered":     COLORS["src_discovered"],
}

# ── Category badge colors ──────────────────────────────────────
CATEGORY_COLORS = {
    "cross_platform": "#10b981",  # green — can be used anywhere
    "native":         "#f59e0b",  # gold — platform-specific
    "installed":      "#3b82f6",  # blue — user-installed
}

# ── Fonts — larger and bolder for readability ──────────────────
FONT_TITLE  = ("Segoe UI", 16, "bold")
FONT_HEADING = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 10)
FONT_CODE   = ("Cascadia Code", 10)
FONT_STAT   = ("Consolas", 12, "bold")
FONT_STAT_NUM = ("Consolas", 24, "bold")
FONT_CARD_NAME = ("Segoe UI", 14, "bold")
FONT_CARD_DESC = ("Segoe UI", 10)
FONT_BADGE  = ("Cascadia Code", 9, "bold")

# ── Dimensions ─────────────────────────────────────────────────
WINDOW_W = 1100
WINDOW_H = 700
SIDEBAR_W = 220
CARD_PAD = 12
SCROLL_SPEED = 20
