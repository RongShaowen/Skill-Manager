#!/usr/bin/env python3
"""Skill Manager — MiMoCode 技能管理器入口"""

import sys
import os

# Ensure we can import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
