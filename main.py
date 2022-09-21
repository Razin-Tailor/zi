import argparse
import curses
import os
import sys
from typing import List


curses.initscr()
curses.start_color()
curses.use_default_colors()

"""
VS Dark Theme
---------------------

#007acc	(0,122,204)
#3e3e42	(62,62,66)
#2d2d30	(45,45,48)
#252526	(37,37,38)
#1e1e1e	(30,30,30)
"""
KEY_ESC = 27
KEY_BACKSPACE = 127
ScreenH = 0
ScreenW = 0
CursorX = 1
CursorY = 1


def set_shorter_esc_delay_in_os():
    os.environ.setdefault("ESCDELAY", "10")


def draw_header(stdscr, width, filename=None, bottom=False):
    VERSION_STR = "v0.1"
    files = ""
    filename = filename or " --- New File --- "

    version_width = len(VERSION_STR) + 2
    if not bottom:
        centered = filename.center(width)[version_width:]
        s = f" zi {VERSION_STR} {files}{centered}"
        stdscr.insstr(0, 0, s, curses.A_REVERSE)
    else:
        centered = " ".center(width)[version_width:]
        s = f"{centered}"
        stdscr.addstr(curses.LINES - 1, 0, s, curses.A_REVERSE)


def open_file(stdscr, filenames: List[str]) -> None:
    ScreenH, ScreenW = stdscr.getmaxyx()
    cloc = "   " + str(CursorX) + ":" + str(CursorY) + " "
    cloclen = len(cloc)
    stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
    dims = stdscr.getmaxyx()

    if len(filenames) > 0:
        for filename in filenames:
            curses.curs_set(0)
            message = filename
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            with open(filename) as f:
                buffer = f.readlines()
            while True:
                stdscr.erase()
                draw_header(stdscr, width=dims[1], filename=filename)
                for row, line in enumerate(buffer):
                    stdscr.addstr(row + 1, 0, line)

                k = stdscr.getch()
                if k == ord("q"):
                    raise SystemExit(0)
                elif k == KEY_EIC:
                    stdscr.addstr(10, 10, os.getenv("ESCDELAY"))

    else:
        draw_header(stdscr, width=dims[1])
        stdscr.move(1, 0)
        curses.echo()
        while True:
            k = stdscr.getch()
            if k == KEY_ESC:
                # draw_header(stdscr, width=dims[1], filename=None, bottom=True)
                stdscr.move(curses.LINES - 1, 0)
                while True:
                    curses.echo()
                    k = stdscr.getch()
                    if k == ord("q"):
                        raise SystemExit(0)

                # cur_y, cur_x = stdscr.getyx()
                # stdscr.move(cur_y, cur_x - 1)
            elif k == KEY_BACKSPACE:
                curses.noecho()
                stdscr.refresh()
                cur_y, cur_x = stdscr.getyx()
                stdscr.move(cur_y, cur_x - 3)


def main(stdscr):
    # print(type(stdscr))
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", default=None, nargs="*")
    args = parser.parse_args()
    # print(args.filename)
    open_file(stdscr, args.filename)


if __name__ == "__main__":
    print(os.environ["TERM"])
    if sys.version_info >= (3, 9) and hasattr(curses, "set_escdelay"):
        curses.set_escdelay(25)
    else:  # pragma: <3.9 cover
        os.environ.setdefault("ESCDELAY", "25")
    curses.wrapper(main)
    # main(None)
