#!/usr/bin/env python3
"""
╔══════════════════════════════════════╗
║          SNAKE-NEO  v2.0             ║
║  Python terminal snake game          ║
╚══════════════════════════════════════╝
Install: https://github.com/NeoInverse/Nokia-Snake
Usage: python snake_neo.py
"""

import curses
import random
import time
import sys
import os
import math
from collections import deque


SNAKE_NEO_LOGO = [
    r"  ██████╗ ███╗   ██╗ █████╗ ██╗  ██╗███████╗  ",
    r" ██╔════╝ ████╗  ██║██╔══██╗██║ ██╔╝██╔════╝  ",
    r" ╚█████╗  ██╔██╗ ██║███████║█████╔╝ █████╗    ",
    r"  ╚═══██╗ ██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝    ",
    r" ██████╔╝ ██║ ╚████║██║  ██║██║  ██╗███████╗  ",
    r" ╚═════╝  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝  ",
]

NEOINVERSE_TITLE = r"  ◈ ─────────  N E O I N V E R S E  ───────── ◈  "

SNAKE_DECO = [
    r"     ╭──────────────────────────────────────╮     ",
    r"     │   ≻══╗  ░░░  ≻══╗  ░░░  ≻══╗  ░░░   │     ",
    r"     │      ╚═══════╝     ╚═══════╝     ╚══╝│     ",
    r"     ╰──────────────────────────────────────╯     ",
]

DEAD_LOGO = [
    r" ██████╗ ███████╗ █████╗ ██████╗  ",
    r" ██╔══██╗██╔════╝██╔══██╗██╔══██╗ ",
    r" ██║  ██║█████╗  ███████║██║  ██║ ",
    r" ██║  ██║██╔══╝  ██╔══██║██║  ██║ ",
    r" ██████╔╝███████╗██║  ██║██████╔╝ ",
    r" ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝  ",
    r"    ║  ║      ║       ║  ║  ║  ║   ",
    r"    ╿  ╿      ╿       ╿  ╿  ╿  ╿   ",
    r"    ▼  ▼      ▼       ▼  ▼  ▼  ▼   ",
]


MAPS = [
    {
        "id": 0,
        "name": "DENSE FOREST",
        "desc": "Classic snake. Trees line the edges.\nHitting walls = DEATH.",
        "wrap": False,
        "border_pair": 35,    
        "bg_pair":     36,   
        "terrain":     "forest",
        "color_theme": "forest",
    },
    {
        "id": 1,
        "name": "DESERT CANYON",
        "desc": "Sandy canyon paths. Maze corridors.\nEdges = DEATH.",
        "wrap": False,
        "border_pair": 37,    # dark yellow
        "bg_pair":     38,    # sand yellow
        "terrain":     "desert",
        "color_theme": "desert",
    },
    {
        "id": 2,
        "name": "STONE CHAMBER",
        "desc": "Dark dungeon with cross obstacles.\nCyan walls. Edges = DEATH.",
        "wrap": False,
        "border_pair": 39,    # dark grey
        "bg_pair":     40,    # dark
        "terrain":     "stone",
        "color_theme": "stone",
    },
    {
        "id": 3,
        "name": "TROPICAL BEACH",
        "desc": "Sandy shore. Ocean corner = DEATH.\nWaves reduce snake & score!",
        "wrap": False,
        "border_pair": 37,
        "bg_pair":     38,
        "terrain":     "beach",
        "color_theme": "beach",
        "ocean_effect": True,
    },
    {
        "id": 4,
        "name": "MATRIX LOOP",
        "desc": "Exit edge → reappear opposite.\nNO BOUNDARY DEATH. Self-bite=DEATH.",
        "wrap": True,
        "border_pair": 28,
        "bg_pair":     0,
        "terrain":     "matrix",
        "color_theme": "matrix",
    },
]

SKINS = [
    {"name": "Emerald",    "head_ch": "◉", "body_ch": "●", "color_id": 1,  "color_id2": 1,  "type": "solid"},
    {"name": "Crimson",    "head_ch": "◉", "body_ch": "●", "color_id": 2,  "color_id2": 2,  "type": "solid"},
    {"name": "Solar",      "head_ch": "◉", "body_ch": "◆", "color_id": 3,  "color_id2": 3,  "type": "solid"},
    {"name": "Ocean",      "head_ch": "◉", "body_ch": "●", "color_id": 4,  "color_id2": 4,  "type": "solid"},
    {"name": "Royal",      "head_ch": "◈", "body_ch": "◇", "color_id": 5,  "color_id2": 5,  "type": "solid"},
    {"name": "Red-White",  "head_ch": "◉", "body_ch": "●", "color_id": 2,  "color_id2": 7,  "type": "alternate"},
    {"name": "Gold-Green", "head_ch": "◉", "body_ch": "◆", "color_id": 3,  "color_id2": 1,  "type": "alternate"},
    {"name": "Cyber",      "head_ch": "◈", "body_ch": "◆", "color_id": 4,  "color_id2": 6,  "type": "alternate"},
    {"name": "Inferno",    "head_ch": "◉", "body_ch": "▪", "color_id": 2,  "color_id2": 3,  "type": "alternate"},
    {"name": "Rainbow",    "head_ch": "◉", "body_ch": "●", "color_id": 1,  "color_id2": 1,  "type": "rainbow"},
]

RAINBOW_PAIRS = [1, 2, 3, 4, 5, 6, 7]   # cycle through these for rainbow skin

UP    = (-1, 0)
DOWN  = (1,  0)
LEFT  = (0, -1)
RIGHT = (0,  1)

def setup_colors():
    curses.start_color()
    curses.use_default_colors()

    # Skin colors
    curses.init_pair(1,  curses.COLOR_GREEN,   -1)
    curses.init_pair(2,  curses.COLOR_RED,     -1)
    curses.init_pair(3,  curses.COLOR_YELLOW,  -1)
    curses.init_pair(4,  curses.COLOR_CYAN,    -1)
    curses.init_pair(5,  curses.COLOR_BLUE,    -1)
    curses.init_pair(6,  curses.COLOR_MAGENTA, -1)
    curses.init_pair(7,  curses.COLOR_WHITE,   -1)

    # UI colors
    curses.init_pair(20, curses.COLOR_WHITE,   -1)
    curses.init_pair(21, curses.COLOR_BLACK,   curses.COLOR_WHITE)
    curses.init_pair(22, curses.COLOR_YELLOW,  -1)
    curses.init_pair(23, curses.COLOR_RED,     -1)
    curses.init_pair(24, curses.COLOR_GREEN,   -1)
    curses.init_pair(25, curses.COLOR_CYAN,    -1)
    curses.init_pair(26, curses.COLOR_MAGENTA, -1)
    curses.init_pair(27, curses.COLOR_WHITE,   curses.COLOR_RED)
    curses.init_pair(28, curses.COLOR_GREEN,   -1)   # matrix
    curses.init_pair(29, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
    curses.init_pair(30, curses.COLOR_WHITE,   curses.COLOR_BLUE)
    curses.init_pair(31, curses.COLOR_BLUE,    -1)   # dim

    # Map terrain colors
    curses.init_pair(35, curses.COLOR_YELLOW,  -1)   # forest border (brown-ish)
    curses.init_pair(36, curses.COLOR_GREEN,   -1)   # forest bg
    curses.init_pair(37, curses.COLOR_YELLOW,  -1)   # desert border
    curses.init_pair(38, curses.COLOR_YELLOW,  -1)   # desert bg
    curses.init_pair(39, curses.COLOR_WHITE,   -1)   # stone border
    curses.init_pair(40, curses.COLOR_WHITE,   -1)   # stone interior
    curses.init_pair(41, curses.COLOR_BLUE,    -1)   # ocean / beach water
    curses.init_pair(42, curses.COLOR_CYAN,    -1)   # wave
    curses.init_pair(43, curses.COLOR_WHITE,   curses.COLOR_BLUE)   # ocean fill
    curses.init_pair(44, curses.COLOR_CYAN,    -1)   # stone walls/obstacles
    curses.init_pair(45, curses.COLOR_GREEN,   -1)   # forest tree
    curses.init_pair(46, curses.COLOR_RED,     -1)   # food on beach


def safe_addstr(win, y, x, text, attr=0):
    h, w = win.getmaxyx()
    if y < 0 or y >= h:
        return
    if x >= w:
        return
    if x < 0:
        text = text[-x:]
        x = 0
    if not text:
        return
    max_len = w - x - 1
    if max_len <= 0:
        return
    try:
        win.addstr(y, x, text[:max_len], attr)
    except curses.error:
        pass

def draw_box(win, y, x, h, w, color_pair):
    safe_addstr(win, y,     x,       "╭" + "─" * (w-2) + "╮", curses.color_pair(color_pair))
    safe_addstr(win, y+h-1, x,       "╰" + "─" * (w-2) + "╯", curses.color_pair(color_pair))
    for i in range(1, h-1):
        safe_addstr(win, y+i, x,       "│", curses.color_pair(color_pair))
        safe_addstr(win, y+i, x+w-1,   "│", curses.color_pair(color_pair))

def draw_centered(win, y, text, attr=0):
    h, w = win.getmaxyx()
    x = max(0, (w - len(text)) // 2)
    safe_addstr(win, y, x, text, attr)

def draw_shift_back(win):
    safe_addstr(win, 0, 1, " ESC: BACK ", curses.color_pair(21) | curses.A_BOLD)

def get_skin_attr(skin, seg_idx, tick):
    """Return curses attr for a snake segment."""
    stype = skin["type"]
    if stype == "solid":
        pid = skin["color_id"]
        attr = curses.color_pair(pid) | curses.A_BOLD
    elif stype == "alternate":
        pid = skin["color_id"] if seg_idx % 2 == 0 else skin["color_id2"]
        attr = curses.color_pair(pid) | curses.A_BOLD
    elif stype == "rainbow":
        pid = RAINBOW_PAIRS[(tick // 2 + seg_idx) % len(RAINBOW_PAIRS)]
        attr = curses.color_pair(pid) | curses.A_BOLD
    else:
        attr = curses.color_pair(1) | curses.A_BOLD
    return attr


def run_intro(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    mid_y = h // 2
    snake_str = "◉●●●●●●●●●●●●●●"
    total_len = len(snake_str)

    for pos in range(-total_len, w + 2):
        stdscr.erase()
        for t in range(pos - 2, pos):
            if 0 <= t < w:
                safe_addstr(stdscr, mid_y, t, "·", curses.color_pair(28))
        for i, ch in enumerate(snake_str):
            x = pos - i
            if 0 <= x < w:
                rainbow_i = RAINBOW_PAIRS[i % len(RAINBOW_PAIRS)]
                attr = curses.color_pair(rainbow_i) | curses.A_BOLD
                safe_addstr(stdscr, mid_y, x, ch, attr)
        stdscr.refresh()
        time.sleep(0.016)

    for tick in range(12):
        stdscr.erase()
        logo_y = max(1, (h - len(SNAKE_NEO_LOGO) - len(SNAKE_DECO) - 5) // 2)
        _rainbow_logo(stdscr, SNAKE_NEO_LOGO, logo_y, tick)
        ni_y = logo_y + len(SNAKE_NEO_LOGO)
        draw_centered(stdscr, ni_y, NEOINVERSE_TITLE,
                      curses.color_pair(RAINBOW_PAIRS[(tick + 2) % len(RAINBOW_PAIRS)]) | curses.A_BOLD)
        deco_y = ni_y + 1
        for i, line in enumerate(SNAKE_DECO):
            draw_centered(stdscr, deco_y + i, line,
                          curses.color_pair(RAINBOW_PAIRS[(tick + i) % len(RAINBOW_PAIRS)]) | curses.A_BOLD)
        draw_centered(stdscr, deco_y + len(SNAKE_DECO) + 1,
                      "  — Press any key to continue —  ",
                      curses.color_pair(20))
        stdscr.refresh()
        time.sleep(0.1)

    stdscr.nodelay(False)
    stdscr.getch()

def _rainbow_logo(win, logo_lines, start_y, tick):
    """Draw logo with smooth sliding gradient (pystyle gradient, tông màu chuyển dần)."""
    h, w = win.getmaxyx()
    gradient = [23, 22, 22, 24, 25, 31, 26, 23, 22, 24, 25]
    plen = len(gradient)
    for i, line in enumerate(logo_lines):
        x = max(0, (w - len(line)) // 2)
        for ci, ch in enumerate(line):
            if x + ci >= w - 1:
                break
            pos = (ci // 5 + i * 2 - tick * 2) % plen
            col = gradient[pos]
            attr = curses.color_pair(col) | curses.A_BOLD
            try:
                win.addstr(start_y + i, x + ci, ch, attr)
            except curses.error:
                pass


def _blood_logo(win, logo_lines, start_y, tick):
    """Draw DEAD logo with blood-red sliding gradient (đỏ gradient, blood chảy xuống)."""
    h, w = win.getmaxyx()
    blood = [2, 23, 27, 23, 2, 23, 27]
    plen = len(blood)
    drip_start = 6   
    for i, line in enumerate(logo_lines):
        x = max(0, (w - len(line)) // 2)
        is_drip = i >= drip_start
        for ci, ch in enumerate(line):
            if x + ci >= w - 1:
                break
            if is_drip:
                blink_off = (tick // 4 + ci) % 3 == 0
                col = 27 if not blink_off else 2
                attr = curses.color_pair(col) | curses.A_BOLD
            else:
                pos = (ci // 4 + i * 3 - tick * 2) % plen
                col = blood[pos]
                attr = curses.color_pair(col) | curses.A_BOLD
            try:
                win.addstr(start_y + i, x + ci, ch, attr)
            except curses.error:
                pass


MENU_ITEMS = ["[ > START ]", "[   SKIN   ]", "[  CREDIT  ]"]

def run_main_menu(stdscr, state):
    curses.curs_set(0)
    stdscr.nodelay(True)
    sel  = state.get("menu_sel", 0)
    tick = 0

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        logo_y = max(1, (h - len(SNAKE_NEO_LOGO) - len(SNAKE_DECO) - 12) // 2)
        _rainbow_logo(stdscr, SNAKE_NEO_LOGO, logo_y, tick // 3)

        ni_y = logo_y + len(SNAKE_NEO_LOGO)
        draw_centered(stdscr, ni_y, NEOINVERSE_TITLE,
                      curses.color_pair(RAINBOW_PAIRS[(tick // 4 + 2) % len(RAINBOW_PAIRS)]) | curses.A_BOLD)

        deco_y = ni_y + 1
        for i, line in enumerate(SNAKE_DECO):
            draw_centered(stdscr, deco_y + i, line,
                          curses.color_pair(RAINBOW_PAIRS[(tick // 4 + i) % len(RAINBOW_PAIRS)]) | curses.A_BOLD)

        menu_y = deco_y + len(SNAKE_DECO) + 2
        for i, item in enumerate(MENU_ITEMS):
            padded = f"  {item}  "
            if i == sel:
                attr = curses.color_pair(21) | curses.A_BOLD
            else:
                attr = curses.color_pair(20)
            draw_centered(stdscr, menu_y + i * 2, padded, attr)

        hint_y = menu_y + len(MENU_ITEMS) * 2 + 1
        draw_centered(stdscr, hint_y,
                      "  PgUp / PgDn : Navigate    Enter : Select  ",
                      curses.color_pair(31))
        safe_addstr(stdscr, h - 2, 2, "SNAKE-NEO v2.0", curses.color_pair(31))

        stdscr.refresh()
        tick += 1
        time.sleep(0.05)

        key = stdscr.getch()
        if key == curses.KEY_PPAGE or key == curses.KEY_UP:
            sel = (sel - 1) % len(MENU_ITEMS)
        elif key == curses.KEY_NPAGE or key == curses.KEY_DOWN:
            sel = (sel + 1) % len(MENU_ITEMS)
        elif key in (10, 13, curses.KEY_ENTER):
            state["menu_sel"] = sel
            return sel
        elif key == 27:
            return -1

# map selection

def run_map_select(stdscr, state):
    curses.curs_set(0)
    stdscr.nodelay(True)
    sel  = state.get("map_sel", 0)
    tick = 0

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        draw_shift_back(stdscr)
        draw_centered(stdscr, 2, "─── SELECT MAP ───",
                      curses.color_pair(22) | curses.A_BOLD)

        n      = len(MAPS)
        box_w  = min(22, (w - 4) // n)
        box_h  = 11
        total_w = n * box_w + (n - 1)
        start_x = max(0, (w - total_w) // 2)
        box_y   = 4

        for i, m in enumerate(MAPS):
            bx = start_x + i * (box_w + 1)
            bp = 22 if i == sel else 31
            draw_box(stdscr, box_y, bx, box_h, box_w, bp)

            name = m["name"][:box_w - 2]
            safe_addstr(stdscr, box_y + 1, bx + max(0, (box_w - len(name)) // 2),
                        name, curses.color_pair(22 if i == sel else 20) | curses.A_BOLD)

            wrap_label = "[WRAP]" if m["wrap"] else "[WALL]"
            safe_addstr(stdscr, box_y + 2, bx + max(0, (box_w - len(wrap_label)) // 2),
                        wrap_label, curses.color_pair(24 if m["wrap"] else 23))

            # mini preview using terrain chars
            pw = box_w - 4
            ph = 5
            for row in range(ph):
                for col in range(pw):
                    px = bx + 2 + col
                    py = box_y + 3 + row
                    if row == 0 or row == ph-1 or col == 0 or col == pw-1:
                        safe_addstr(stdscr, py, px, "█",
                                    curses.color_pair(m["border_pair"]))
                    else:
                        t = m["terrain"]
                        if t == "forest":
                            ch = "♣" if (row + col) % 4 == 0 else "·"
                            safe_addstr(stdscr, py, px, ch, curses.color_pair(45))
                        elif t == "desert":
                            ch = "░" if (row + col) % 2 == 0 else " "
                            safe_addstr(stdscr, py, px, ch, curses.color_pair(38))
                        elif t == "stone":
                            ch = "+" if (row == ph//2 or col == pw//2) else "."
                            safe_addstr(stdscr, py, px, ch, curses.color_pair(44))
                        elif t == "beach":
                            if row < 2 and col < pw // 3:
                                safe_addstr(stdscr, py, px, "≈", curses.color_pair(41))
                            else:
                                safe_addstr(stdscr, py, px, "·", curses.color_pair(38))
                        elif t == "matrix":
                            safe_addstr(stdscr, py, px,
                                        str(random.randint(0,1)) if random.random() < 0.3 else " ",
                                        curses.color_pair(28))

            for di, dl in enumerate(m["desc"].split("\n")[:2]):
                safe_addstr(stdscr, box_y + box_h + di, bx + 1, dl.strip()[:box_w-2],
                            curses.color_pair(20))

        draw_centered(stdscr, box_y + box_h + 3,
                      "  ← → : Navigate    Enter : Confirm  ",
                      curses.color_pair(31))

        stdscr.refresh()
        tick += 1
        time.sleep(0.06)

        key = stdscr.getch()
        if key in (curses.KEY_LEFT, curses.KEY_HOME):
            sel = (sel - 1) % n
        elif key in (curses.KEY_RIGHT, curses.KEY_END):
            sel = (sel + 1) % n
        elif key in (10, 13, curses.KEY_ENTER):
            state["map_sel"] = sel
            return sel
        elif key == 27:
            return -1

# skin selection

def draw_skin_preview(win, y, x, skin, selected, tick):
    box_w = 15
    box_h = 6
    bp    = 22 if selected else 31
    draw_box(win, y, x, box_h, box_w, bp)

    if selected:
        try:
            win.addstr(y,       x, "╭" + "═" * (box_w-2) + "╮",
                       curses.color_pair(22) | curses.A_BOLD)
            win.addstr(y+box_h-1, x, "╰" + "═" * (box_w-2) + "╯",
                       curses.color_pair(22) | curses.A_BOLD)
        except curses.error:
            pass

    # Animated snake segments inside box
    segments = [
        (y+1, x+10), (y+1, x+9), (y+1, x+8),
        (y+2, x+8),  (y+3, x+8), (y+3, x+7), (y+3, x+6),
    ]
    for si, (sy, sx) in enumerate(segments):
        ch   = skin["head_ch"] if si == 0 else skin["body_ch"]
        attr = get_skin_attr(skin, si, tick)
        safe_addstr(win, sy, sx, ch, attr)

    name = skin["name"][:box_w-2]
    nx_  = x + max(0, (box_w - len(name)) // 2)
    safe_addstr(win, y + box_h - 1, nx_, name,
                curses.color_pair(22 if selected else 20))

def run_skin_select(stdscr, state):
    curses.curs_set(0)
    stdscr.nodelay(True)
    sel  = state.get("skin_sel", 0)
    tick = 0
    cols = 5
    rows = 2

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        draw_shift_back(stdscr)
        draw_centered(stdscr, 2, "─── SELECT SKIN ───",
                      curses.color_pair(22) | curses.A_BOLD)

        box_w = 15
        box_h = 7
        sx_sp = 2
        sy_sp = 2

        grid_w  = cols * box_w + (cols-1) * sx_sp
        start_x = max(0, (w - grid_w) // 2)
        start_y = 5

        for i, skin in enumerate(SKINS):
            row = i // cols
            col = i % cols
            sy  = start_y + row * (box_h + sy_sp)
            sx  = start_x + col * (box_w + sx_sp)
            draw_skin_preview(stdscr, sy, sx, skin, i == sel, tick)

        cur_name = SKINS[sel]["name"]
        draw_centered(stdscr, start_y + rows * (box_h + sy_sp) + 1,
                      f"  Selected: [ {cur_name} ]  ",
                      curses.color_pair(26) | curses.A_BOLD)
        draw_centered(stdscr, start_y + rows * (box_h + sy_sp) + 3,
                      "  ← → ↑ ↓ : Navigate    Enter : Confirm    ESC : Back  ",
                      curses.color_pair(31))

        stdscr.refresh()
        tick += 1
        time.sleep(0.05)

        key = stdscr.getch()
        cur_row = sel // cols
        cur_col = sel % cols
        if key == curses.KEY_LEFT:
            sel = (sel - 1) % len(SKINS)
        elif key == curses.KEY_RIGHT:
            sel = (sel + 1) % len(SKINS)
        elif key == curses.KEY_UP:
            sel = ((cur_row - 1) % rows) * cols + cur_col
        elif key == curses.KEY_DOWN:
            sel = ((cur_row + 1) % rows) * cols + cur_col
        elif key in (10, 13, curses.KEY_ENTER):
            state["skin_sel"] = sel
            return sel
        elif key == 27:
            return -1

# credit
def run_credits(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    tick = 0

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        draw_shift_back(stdscr)

        logo_y = max(1, h // 2 - len(SNAKE_NEO_LOGO) // 2 - 7)
        _rainbow_logo(stdscr, SNAKE_NEO_LOGO, logo_y, tick // 3)

        ni_y = logo_y + len(SNAKE_NEO_LOGO)
        draw_centered(stdscr, ni_y, NEOINVERSE_TITLE,
                      curses.color_pair(RAINBOW_PAIRS[(tick // 4 + 2) % len(RAINBOW_PAIRS)]) | curses.A_BOLD)

        info_y = ni_y + 2
        credits_lines = [
            ("┌───────────────────────────────────────┐", 25),
            ("│                                       │", 25),
            ("│   AUTHOR:  'Tr Nhật Bảo Nam'          │", 22),
            ("│                                       │", 25),
            ("│   TEAM:  'NeoInverse'                 │", 26),
            ("│                                       │", 25),
            ("│   GIT:  'NeoInverse/Nokia-Snake'      │", 24),
            ("│                                       │", 25),
            ("└───────────────────────────────────────┘", 25),
        ]
        for i, (line, pair) in enumerate(credits_lines):
            draw_centered(stdscr, info_y + i, line,
                          curses.color_pair(pair) | curses.A_BOLD)
        draw_centered(stdscr, info_y + len(credits_lines) + 2,
                      "  ESC : Back to Menu  ", curses.color_pair(31))

        stdscr.refresh()
        tick += 1
        time.sleep(0.06)

        key = stdscr.getch()
        if key == 27 or key == curses.KEY_PPAGE:
            return

class GameState:
    def __init__(self, map_def, skin):
        self.map_def         = map_def
        self.skin            = skin
        self.score           = 0
        self.small_eaten     = 0
        self.big_food_active = False
        self.big_food_pos    = None
        self.big_food_timer  = 0.0
        self.BIG_FOOD_TTL    = 7.0
        self.foods           = []
        self.MAX_FOODS       = 3
        self.snake           = deque()
        self.direction       = RIGHT
        self.next_direction  = RIGHT
        self.grow_queue      = 0
        self.dead            = False
        self.elapsed         = 0.0
        self.start_time      = time.time()
        self.obstacles       = set()   # (r, c) positions that are walls
        self.tick            = 0

        # Tropical Beach wave state
        self.ocean_corner     = 0           # 0=TL, 1=TR, 2=BL, 3=BR
        self.wave_active      = False
        self.wave_cells       = []          
        self.wave_dir         = None
        self.wave_timer       = 0.0
        self.wave_speed       = 0.12        # seconds per wave step
        self.wave_last_step   = 0.0
        self.food_since_wave  = 0           # eaten since last wave
        self.wave_trigger     = random.randint(5, 6)

        # Ocean zone cells (set by build_map)
        self.ocean_cells      = set()
        self.grid_h           = 0
        self.grid_w           = 0

        # Stone Chamber bombs
        self.bombs            = []         
        self.BOMB_TTL         = 3.0         # seconds before explosion
        self.BOMB_BLAST_R     = 2           # blast radius in cells (Manhattan)
        self.stone_food_count = 0           # small food eaten since last bomb drop
        self.bomb_trigger     = random.randint(5, 6)  

    def init_snake(self, grid_h, grid_w):
        self.grid_h = grid_h
        self.grid_w = grid_w
        mid_r = grid_h // 2
        mid_c = grid_w // 2

        spawn_r, spawn_c = mid_r, mid_c
        if self.obstacles:
            found = False
            for try_r in range(2, grid_h - 2):
                for try_c in range(6, grid_w - 6):
                    if all((try_r, try_c - i) not in self.obstacles for i in range(5)):
                        spawn_r, spawn_c = try_r, try_c
                        found = True
                        break
                if found:
                    break

        for i in range(5):
            self.snake.append((spawn_r, spawn_c - i))

    def build_map(self, grid_h, grid_w):
        """Build obstacle set and ocean zone for this map."""
        self.obstacles.clear()
        self.ocean_cells.clear()
        terrain = self.map_def["terrain"]

        if terrain == "forest":
            self._build_forest(grid_h, grid_w)
        elif terrain == "desert":
            self._build_desert(grid_h, grid_w)
        elif terrain == "stone":
            self._build_stone(grid_h, grid_w)
        elif terrain == "beach":
            self._build_beach(grid_h, grid_w)

    def _build_forest(self, h, w):
        # Trees every 4 cells in a grid pattern, skipping center area
        cx, cy = w // 2, h // 2
        for r in range(3, h - 3, 4):
            for c in range(4, w - 4, 4):
                if abs(r - cy) + abs(c - cx) > 6:   # leave center clear
                    self.obstacles.add((r, c))

    def _build_desert(self, h, w):
        # Desert canyon: maze-like L-shaped and C-shaped walls
        cx, cy = w // 2, h // 2
        # Outer ring gaps (like canyon walls)
        for r in range(4, h - 4, 8):
            for c in range(5, w - 5, 8):
                # C-shape
                for dr in range(3):
                    self.obstacles.add((r + dr, c))
                for dc in range(3):
                    self.obstacles.add((r, c + dc))
                for dr in range(3):
                    self.obstacles.add((r + dr, c + 2))

    def _build_stone(self, h, w):
        positions = [
            (h // 4,     w // 3),
            (h // 4,     2 * w // 3),
            (h // 2,     w // 2),
            (3 * h // 4, w // 3),
            (3 * h // 4, 2 * w // 3),
        ]
        for cr, cc in positions:
            for dr in range(-2, 3):
                r = cr + dr
                if 2 <= r < h - 2:
                    self.obstacles.add((r, cc))
            for dc in range(-2, 3):
                c = cc + dc
                if 2 <= c < w - 2:
                    self.obstacles.add((cr, c))

    def _build_beach(self, h, w):
        self._update_ocean_zone(h, w)

    def _update_ocean_zone(self, h, w):
        """Update ocean zone based on current corner."""
        self.ocean_cells.clear()
        ow = max(6, w // 5)
        oh = max(4, h // 5)
        corner = self.ocean_corner % 4
        if corner == 0:   # top-left
            r0, c0 = 1, 1
        elif corner == 1:  # top-right
            r0, c0 = 1, w - 1 - ow
        elif corner == 2:  # bottom-left
            r0, c0 = h - 1 - oh, 1
        else:              # bottom-right
            r0, c0 = h - 1 - oh, w - 1 - ow
        for r in range(r0, r0 + oh):
            for c in range(c0, c0 + ow):
                if 1 <= r < h - 1 and 1 <= c < w - 1:
                    self.ocean_cells.add((r, c))

    def spawn_food(self, grid_h, grid_w):
        occupied = set(self.snake)
        if self.big_food_pos:
            occupied.add(self.big_food_pos)
        occupied.update(self.foods)
        occupied.update(self.obstacles)
        occupied.update(self.ocean_cells)
        attempts = 0
        while len(self.foods) < self.MAX_FOODS and attempts < 300:
            r = random.randint(1, grid_h - 2)
            c = random.randint(1, grid_w - 2)
            if (r, c) not in occupied:
                self.foods.append((r, c))
                occupied.add((r, c))
            attempts += 1

    def spawn_big_food(self, grid_h, grid_w):
        occupied = set(self.snake)
        occupied.update(self.foods)
        occupied.update(self.obstacles)
        occupied.update(self.ocean_cells)
        for _ in range(300):
            r = random.randint(1, grid_h - 2)
            c = random.randint(1, grid_w - 2)
            if (r, c) not in occupied:
                self.big_food_pos    = (r, c)
                self.big_food_timer  = time.time()
                self.big_food_active = True
                return

    def spawn_wave(self, grid_h, grid_w):
        """Spawn a wave from the ocean corner, directed inward into the map."""
        if not self.ocean_cells:
            return
        # Pick a random ocean edge cell as origin
        origin = random.choice(list(self.ocean_cells))
        corner = self.ocean_corner % 4
        if corner == 0:
            valid_dirs = [DOWN, RIGHT, (1, 1)]
        elif corner == 1:
            valid_dirs = [DOWN, LEFT, (1, -1)]
        elif corner == 2:
            valid_dirs = [UP, RIGHT, (-1, 1)]
        else:
            valid_dirs = [UP, LEFT, (-1, -1)]
        d = random.choice(valid_dirs)
        # Wave width: 3 cells perpendicular
        self.wave_cells = [origin]
        r0, c0 = origin
        dr, dc = d
        if dr != 0 and dc == 0:
            perp = [(r0, c0 - 1), (r0, c0 + 1)]
        elif dc != 0 and dr == 0:
            perp = [(r0 - 1, c0), (r0 + 1, c0)]
        else:
            perp = [(r0 + dc, c0), (r0, c0 + dr)]
        for pr, pc in perp:
            if 0 <= pr < grid_h and 0 <= pc < grid_w:
                self.wave_cells.append((pr, pc))
        self.wave_dir       = d
        self.wave_active    = True
        self.wave_last_step = time.time()

    def step_wave(self, grid_h, grid_w):
        """Move wave one step in its direction."""
        dr, dc = self.wave_dir
        new_cells = []
        for r, c in self.wave_cells:
            nr, nc = r + dr, c + dc
            if 0 < nr < grid_h - 1 and 0 < nc < grid_w - 1:
                new_cells.append((nr, nc))
        if not new_cells:
            self.wave_active = False
            self.wave_cells  = []
            # Move ocean to next corner
            self.ocean_corner = (self.ocean_corner + 1) % 4
            self._update_ocean_zone(grid_h, grid_w)
        else:
            self.wave_cells = new_cells

    def apply_wave_penalty(self):
        """Remove 40% of snake body and 40% of score."""
        remove_n = max(1, int(len(self.snake) * 0.4))
        for _ in range(remove_n):
            if len(self.snake) > 1:
                self.snake.pop()
        self.score = max(0, int(self.score * 0.6))

    def spawn_bombs(self, grid_h, grid_w):
        """Spawn 2 bombs at random clear positions (stone map)."""
        occupied = set(self.snake)
        occupied.update(self.foods)
        occupied.update(self.obstacles)
        if self.big_food_pos:
            occupied.add(self.big_food_pos)
        for bm in self.bombs:
            occupied.add(bm["pos"])
        for _ in range(2):
            for _ in range(400):
                r = random.randint(2, grid_h - 3)
                c = random.randint(2, grid_w - 3)
                if (r, c) not in occupied:
                    self.bombs.append({"pos": (r, c), "timer": time.time()})
                    occupied.add((r, c))
                    break

    def apply_bomb_penalty(self):
        """Snake loses 50% length and 50% score when caught in a blast."""
        remove_n = len(self.snake) // 2
        for _ in range(remove_n):
            if len(self.snake) > 1:
                self.snake.pop()
        self.score = max(0, self.score // 2)


def _ocean_corner_coords(gs, grid_h, grid_w):
    ow = max(6, grid_w // 5)
    oh = max(4, grid_h // 5)
    corner = gs.ocean_corner % 4
    if corner == 0:
        r0, c0 = 1, 1
    elif corner == 1:
        r0, c0 = 1, grid_w - 1 - ow
    elif corner == 2:
        r0, c0 = grid_h - 1 - oh, 1
    else:
        r0, c0 = grid_h - 1 - oh, grid_w - 1 - ow
    return r0, c0, oh, ow


def draw_map_interior(stdscr, gs, oy, ox, grid_h, grid_w, tick):
    """Draw the map background, terrain features, and obstacles."""
    terrain = gs.map_def["terrain"]

    if terrain == "forest":
        _draw_forest(stdscr, gs, oy, ox, grid_h, grid_w, tick)
    elif terrain == "desert":
        _draw_desert(stdscr, gs, oy, ox, grid_h, grid_w, tick)
    elif terrain == "stone":
        _draw_stone(stdscr, gs, oy, ox, grid_h, grid_w, tick)
    elif terrain == "beach":
        _draw_beach(stdscr, gs, oy, ox, grid_h, grid_w, tick)
    elif terrain == "matrix":
        _draw_matrix(stdscr, gs, oy, ox, grid_h, grid_w, tick)


def _draw_border(stdscr, oy, ox, grid_h, grid_w, border_ch, border_pair):
    for r in range(grid_h):
        for c in range(grid_w):
            if r == 0 or r == grid_h-1 or c == 0 or c == grid_w-1:
                safe_addstr(stdscr, oy + r, ox + c, border_ch,
                            curses.color_pair(border_pair) | curses.A_BOLD)


def _draw_forest(stdscr, gs, oy, ox, grid_h, grid_w, tick):
    for r in range(1, grid_h - 1):
        for c in range(1, grid_w - 1):
            safe_addstr(stdscr, oy + r, ox + c, "·",
                        curses.color_pair(36))

    for (r, c) in gs.obstacles:
        if 1 <= r < grid_h - 1 and 1 <= c < grid_w - 1:
            safe_addstr(stdscr, oy + r, ox + c, "♣",
                        curses.color_pair(45) | curses.A_BOLD)

    for r in range(grid_h):
        for c in range(grid_w):
            if r == 0 or r == grid_h - 1 or c == 0 or c == grid_w - 1:
                safe_addstr(stdscr, oy + r, ox + c, "▓",
                            curses.color_pair(35) | curses.A_BOLD)


def _draw_desert(stdscr, gs, oy, ox, grid_h, grid_w, tick):
    for r in range(1, grid_h - 1):
        for c in range(1, grid_w - 1):
            ch = "░" if (r + c) % 3 == 0 else " "
            safe_addstr(stdscr, oy + r, ox + c, ch,
                        curses.color_pair(38))

    for (r, c) in gs.obstacles:
        if 1 <= r < grid_h - 1 and 1 <= c < grid_w - 1:
            safe_addstr(stdscr, oy + r, ox + c, "▓",
                        curses.color_pair(37) | curses.A_BOLD)

    for r in range(grid_h):
        for c in range(grid_w):
            if r == 0 or r == grid_h - 1 or c == 0 or c == grid_w - 1:
                safe_addstr(stdscr, oy + r, ox + c, "═",
                            curses.color_pair(37) | curses.A_BOLD)


def _draw_stone(stdscr, gs, oy, ox, grid_h, grid_w, tick):
    for r in range(1, grid_h - 1):
        for c in range(1, grid_w - 1):
            ch = "·" if (r * 3 + c * 2) % 7 == 0 else " "
            safe_addstr(stdscr, oy + r, ox + c, ch,
                        curses.color_pair(31))

    for (r, c) in gs.obstacles:
        if 1 <= r < grid_h - 1 and 1 <= c < grid_w - 1:
            safe_addstr(stdscr, oy + r, ox + c, "╬",
                        curses.color_pair(44) | curses.A_BOLD)

    for r in range(grid_h):
        for c in range(grid_w):
            if r == 0 or r == grid_h - 1 or c == 0 or c == grid_w - 1:
                safe_addstr(stdscr, oy + r, ox + c, "█",
                            curses.color_pair(39) | curses.A_BOLD)


def _draw_beach(stdscr, gs, oy, ox, grid_h, grid_w, tick):
    for r in range(1, grid_h - 1):
        for c in range(1, grid_w - 1):
            ch = "·" if (r + c) % 4 == 0 else " "
            safe_addstr(stdscr, oy + r, ox + c, ch,
                        curses.color_pair(38))

    blink = (tick // 4) % 2
    for (r, c) in gs.ocean_cells:
        ch = "≈" if blink == 0 else "~"
        safe_addstr(stdscr, oy + r, ox + c, ch,
                    curses.color_pair(43) | curses.A_BOLD)

    if gs.wave_active:
        wave_blink = (tick // 2) % 2
        wch = "∿" if wave_blink == 0 else "≋"
        for (wr, wc) in gs.wave_cells:
            if 0 < wr < grid_h and 0 < wc < grid_w:
                safe_addstr(stdscr, oy + wr, ox + wc, wch,
                            curses.color_pair(42) | curses.A_BOLD)

    for r in range(grid_h):
        for c in range(grid_w):
            if r == 0 or r == grid_h - 1 or c == 0 or c == grid_w - 1:
                safe_addstr(stdscr, oy + r, ox + c, "≈",
                            curses.color_pair(41) | curses.A_BOLD)


def _draw_matrix(stdscr, gs, oy, ox, grid_h, grid_w, tick):
    for r in range(1, grid_h - 1):
        for c in range(1, grid_w - 1):
            if random.random() < 0.006:
                safe_addstr(stdscr, oy + r, ox + c,
                            str(random.randint(0, 1)),
                            curses.color_pair(28))

    for r in range(grid_h):
        for c in range(grid_w):
            if r == 0 or r == grid_h - 1:
                safe_addstr(stdscr, oy + r, ox + c, "─",
                            curses.color_pair(28) | curses.A_BOLD)
            elif c == 0 or c == grid_w - 1:
                safe_addstr(stdscr, oy + r, ox + c, "│",
                            curses.color_pair(28) | curses.A_BOLD)


def run_game_with_score(stdscr, map_idx, skin_idx, state):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    map_def = MAPS[map_idx]
    skin    = SKINS[skin_idx]

    h, w = stdscr.getmaxyx()
    GRID_H = min(28, h - 8)
    GRID_W = min(58, w - 20)
    if GRID_H < 10: GRID_H = 10
    if GRID_W < 20: GRID_W = 20

    GRID_OY = max(5, (h - GRID_H) // 2)
    GRID_OX = max(10, (w - GRID_W) // 2)

    gs = GameState(map_def, skin)
    gs.build_map(GRID_H, GRID_W)    
    gs.init_snake(GRID_H, GRID_W)
    gs.spawn_food(GRID_H, GRID_W)

    SPEED_H  = 0.10   # seconds per tick when moving left/right
    SPEED_V  = 0.15   # seconds per tick when moving up/down
    last_move = time.time()
    tick      = 0

    big_food_blink = 0

    while True:
        now = time.time()
        gs.elapsed = now - gs.start_time
        gs.tick    = tick

        key = stdscr.getch()
        if key == 27:
            state["last_score"] = gs.score
            return "quit"
        elif key == curses.KEY_UP    and gs.direction != DOWN:
            gs.next_direction = UP
        elif key == curses.KEY_DOWN  and gs.direction != UP:
            gs.next_direction = DOWN
        elif key == curses.KEY_LEFT  and gs.direction != RIGHT:
            gs.next_direction = LEFT
        elif key == curses.KEY_RIGHT and gs.direction != LEFT:
            gs.next_direction = RIGHT

        cur_speed = SPEED_V if gs.direction in (UP, DOWN) else SPEED_H

        if now - last_move >= cur_speed:
            last_move = now
            gs.direction = gs.next_direction
            dr, dc = gs.direction
            head_r, head_c = gs.snake[0]
            nr, nc = head_r + dr, head_c + dc

            if map_def["wrap"]:
                nr = nr % GRID_H
                nc = nc % GRID_W
            else:
                if nr <= 0 or nr >= GRID_H - 1 or nc <= 0 or nc >= GRID_W - 1:
                    gs.dead = True

            # Obstacle collision
            if (nr, nc) in gs.obstacles:
                gs.dead = True

            # Ocean zone collision (beach map)
            if not gs.dead and map_def["terrain"] == "beach":
                if (nr, nc) in gs.ocean_cells:
                    gs.dead = True

            # Self-collision
            if not gs.dead and (nr, nc) in gs.snake:
                gs.dead = True

            if gs.dead:
                state["last_score"] = gs.score
                return "dead"

            gs.snake.appendleft((nr, nc))
            if gs.grow_queue > 0:
                gs.grow_queue -= 1
            else:
                gs.snake.pop()

            # Check wave hit
            if gs.wave_active and (nr, nc) in gs.wave_cells:
                gs.apply_wave_penalty()

            # Small food
            if (nr, nc) in gs.foods:
                gs.foods.remove((nr, nc))
                gs.score       += 5
                gs.grow_queue  += 1
                gs.small_eaten += 1
                gs.food_since_wave  += 1
                gs.stone_food_count += 1
                gs.spawn_food(GRID_H, GRID_W)
                if gs.small_eaten % 10 == 0 and not gs.big_food_active:
                    gs.spawn_big_food(GRID_H, GRID_W)
                # Beach wave trigger
                if map_def["terrain"] == "beach":
                    if gs.food_since_wave >= gs.wave_trigger and not gs.wave_active:
                        gs.spawn_wave(GRID_H, GRID_W)
                        gs.food_since_wave = 0
                        gs.wave_trigger    = random.randint(5, 6)
                # Stone bomb trigger
                if map_def["terrain"] == "stone":
                    if gs.stone_food_count >= gs.bomb_trigger:
                        gs.spawn_bombs(GRID_H, GRID_W)
                        gs.stone_food_count = 0
                        gs.bomb_trigger     = random.randint(5, 6)

            # Big food
            if gs.big_food_active and gs.big_food_pos == (nr, nc):
                gs.score          += 15
                gs.grow_queue     += 3
                gs.food_since_wave += 1
                gs.big_food_active = False
                gs.big_food_pos    = None
                if map_def["terrain"] == "beach":
                    if gs.food_since_wave >= gs.wave_trigger and not gs.wave_active:
                        gs.spawn_wave(GRID_H, GRID_W)
                        gs.food_since_wave = 0
                        gs.wave_trigger    = random.randint(5, 6)

        # Big food expiry
        if gs.big_food_active:
            if time.time() - gs.big_food_timer >= gs.BIG_FOOD_TTL:
                gs.big_food_active = False
                gs.big_food_pos    = None

        # Wave step
        if gs.wave_active:
            if time.time() - gs.wave_last_step >= gs.wave_speed:
                gs.wave_last_step = time.time()
                gs.step_wave(GRID_H, GRID_W)

        # Bomb explosions (stone map)
        if map_def["terrain"] == "stone" and gs.bombs:
            now_b = time.time()
            surviving = []
            penalty_applied = False
            for bm in gs.bombs:
                if now_b - bm["timer"] >= gs.BOMB_TTL:
                    # Explode: check if any snake segment is within blast radius
                    br, bc = bm["pos"]
                    hit = any(
                        abs(sr - br) + abs(sc - bc) <= gs.BOMB_BLAST_R
                        for sr, sc in gs.snake
                    )
                    if hit and not penalty_applied:
                        gs.apply_bomb_penalty()
                        penalty_applied = True
                    # Bomb is consumed (exploded), do not keep it
                else:
                    surviving.append(bm)
            gs.bombs = surviving

        # draw
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        GRID_OY = max(5, (h - GRID_H) // 2)
        GRID_OX = max(10, (w - GRID_W) // 2)

        # HUD
        hud_y = GRID_OY - 3
        safe_addstr(stdscr, hud_y, GRID_OX,
                    f"  SCORE: {gs.score:04d}  ",
                    curses.color_pair(22) | curses.A_BOLD)
        safe_addstr(stdscr, hud_y, GRID_OX + 16,
                    f"  MAP: {map_def['name']}  ",
                    curses.color_pair(25) | curses.A_BOLD)

        # Timer bar
        timer_y = GRID_OY - 2
        if gs.big_food_active:
            elapsed_big = time.time() - gs.big_food_timer
            ratio       = max(0.0, 1.0 - elapsed_big / gs.BIG_FOOD_TTL)
            bar_total   = GRID_W - 22
            filled      = int(bar_total * ratio)
            bar         = "█" * filled + "░" * (bar_total - filled)
            label       = " ◆ BIG FOOD: "
            safe_addstr(stdscr, timer_y, GRID_OX, label,
                        curses.color_pair(26) | curses.A_BOLD)
            safe_addstr(stdscr, timer_y, GRID_OX + len(label), bar,
                        curses.color_pair(29) | curses.A_BOLD)
            safe_addstr(stdscr, timer_y, GRID_OX + len(label) + bar_total + 1,
                        f" {max(0.0, gs.BIG_FOOD_TTL - elapsed_big):.1f}s ",
                        curses.color_pair(26) | curses.A_BOLD)
        else:
            count_down = 10 - (gs.small_eaten % 10) if gs.small_eaten > 0 else 10
            safe_addstr(stdscr, timer_y, GRID_OX,
                        f"  Eat {count_down} more ★ for ◆ big food  ",
                        curses.color_pair(31))

        # Beach wave warning
        if map_def["terrain"] == "beach":
            wave_y = GRID_OY - 1
            if gs.wave_active:
                safe_addstr(stdscr, wave_y, GRID_OX,
                            "  ∿∿∿ WAVE INCOMING! Duck! ∿∿∿  ",
                            curses.color_pair(42) | curses.A_BOLD)
            else:
                left = gs.wave_trigger - gs.food_since_wave
                safe_addstr(stdscr, wave_y, GRID_OX,
                            f"  Next wave in: {left} food  ",
                            curses.color_pair(31))

        # Stone bomb HUD
        if map_def["terrain"] == "stone":
            bomb_hud_y = GRID_OY - 1
            if gs.bombs:
                safe_addstr(stdscr, bomb_hud_y, GRID_OX,
                            "  ✦ BOMBS ACTIVE! Stay away!  ",
                            curses.color_pair(23) | curses.A_BOLD)
            else:
                left_b = gs.bomb_trigger - gs.stone_food_count
                safe_addstr(stdscr, bomb_hud_y, GRID_OX,
                            f"  Next bombs in: {left_b} food  ",
                            curses.color_pair(31))

        # Map terrain
        draw_map_interior(stdscr, gs, GRID_OY, GRID_OX, GRID_H, GRID_W, tick)

        # Small foods
        for fr, fc in gs.foods:
            safe_addstr(stdscr, GRID_OY + fr, GRID_OX + fc,
                        "★", curses.color_pair(22) | curses.A_BOLD)

        # Big food blinking
        big_food_blink = (big_food_blink + 1) % 8
        if gs.big_food_active and gs.big_food_pos:
            bfr, bfc = gs.big_food_pos
            sp = 26 if big_food_blink < 4 else 23
            safe_addstr(stdscr, GRID_OY + bfr, GRID_OX + bfc,
                        "◆", curses.color_pair(sp) | curses.A_BOLD)

        # Bombs (stone map) — blink faster as countdown nears zero
        if map_def["terrain"] == "stone":
            now_draw = time.time()
            for bm in gs.bombs:
                br, bc = bm["pos"]
                remaining = gs.BOMB_TTL - (now_draw - bm["timer"])
                # Blink rate: slow when safe, fast when about to blow
                blink_rate = 6 if remaining > 2.0 else (3 if remaining > 1.0 else 1)
                blink_on   = (tick // blink_rate) % 2 == 0
                bm_col     = 27 if blink_on else 23   # white-on-red ↔ red
                safe_addstr(stdscr, GRID_OY + br, GRID_OX + bc,
                            "✦", curses.color_pair(bm_col) | curses.A_BOLD)
                # Countdown digit (1-char) to the right of the bomb if room
                cd = max(1, int(remaining) + 1)
                if bc + 1 < GRID_W - 1:
                    safe_addstr(stdscr, GRID_OY + br, GRID_OX + bc + 1,
                                str(cd), curses.color_pair(22) | curses.A_BOLD)
                # Show blast-radius ring when < 1 s left
                if remaining < 1.0:
                    for dr_ in range(-gs.BOMB_BLAST_R, gs.BOMB_BLAST_R + 1):
                        for dc_ in range(-gs.BOMB_BLAST_R, gs.BOMB_BLAST_R + 1):
                            if abs(dr_) + abs(dc_) == gs.BOMB_BLAST_R:
                                rr, rc = br + dr_, bc + dc_
                                if 1 <= rr < GRID_H - 1 and 1 <= rc < GRID_W - 1:
                                    safe_addstr(stdscr, GRID_OY + rr, GRID_OX + rc,
                                                "░", curses.color_pair(23))

        # Snake — draw with skin-specific colors
        for idx, (sr, sc) in enumerate(gs.snake):
            ch   = skin["head_ch"] if idx == 0 else skin["body_ch"]
            attr = get_skin_attr(skin, idx, tick)
            safe_addstr(stdscr, GRID_OY + sr, GRID_OX + sc, ch, attr)

        # Hint
        safe_addstr(stdscr, GRID_OY + GRID_H + 1, GRID_OX,
                    "  ESC: Quit   ↑↓←→: Move   ★+5pts   ◆+15pts  ",
                    curses.color_pair(31))

        stdscr.refresh()
        tick += 1
        time.sleep(0.01)


def run_death_screen(stdscr, score):
    curses.curs_set(0)
    stdscr.nodelay(True)
    sel  = 0
    tick = 0
    OPTIONS = ["[ > REPLAY ]", "[ BACK TO LOBBY ]"]

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        logo_y = max(1, h // 2 - len(DEAD_LOGO) // 2 - 5)
        _blood_logo(stdscr, DEAD_LOGO, logo_y, tick)

        score_y = logo_y + len(DEAD_LOGO) + 1
        draw_centered(stdscr, score_y, f"  FINAL SCORE: {score}  ",
                      curses.color_pair(22) | curses.A_BOLD)

        opt_y = score_y + 2
        for i, opt in enumerate(OPTIONS):
            attr = curses.color_pair(21) | curses.A_BOLD if i == sel else curses.color_pair(20)
            draw_centered(stdscr, opt_y + i * 2, f"  {opt}  ", attr)

        draw_centered(stdscr, opt_y + len(OPTIONS) * 2 + 1,
                      "  PgUp / PgDn : Navigate    Enter : Select  ",
                      curses.color_pair(31))

        stdscr.refresh()
        tick += 1
        time.sleep(0.05)

        key = stdscr.getch()
        if key in (curses.KEY_PPAGE, curses.KEY_UP):
            sel = (sel - 1) % len(OPTIONS)
        elif key in (curses.KEY_NPAGE, curses.KEY_DOWN):
            sel = (sel + 1) % len(OPTIONS)
        elif key in (10, 13, curses.KEY_ENTER):
            return "replay" if sel == 0 else "lobby"
        elif key == 27:
            return "lobby"

def main_fixed(stdscr):
    setup_colors()
    curses.curs_set(0)
    stdscr.keypad(True)

    state = {
        "menu_sel":   0,
        "map_sel":    0,
        "skin_sel":   0,
        "last_score": 0,
    }

    run_intro(stdscr)

    while True:
        choice = run_main_menu(stdscr, state)

        if choice == -1:
            break

        elif choice == 0:  # START
            map_idx = run_map_select(stdscr, state)
            if map_idx == -1:
                continue

            while True:
                result = run_game_with_score(stdscr, map_idx, state["skin_sel"], state)
                if result == "quit":
                    break
                elif result == "dead":
                    death_result = run_death_screen(stdscr, state["last_score"])
                    if death_result == "replay":
                        continue
                    else:
                        break

        elif choice == 1:
            run_skin_select(stdscr, state)

        elif choice == 2:
            run_credits(stdscr)

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    sys.stdout.write("\033[2J")
    sys.stdout.flush()
    try:
        curses.wrapper(main_fixed)
    except KeyboardInterrupt:
        pass
    finally:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n  Thanks for playing SNAKE-NEO!\n")
