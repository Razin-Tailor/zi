import argparse
import curses

def open_file(stdscr, filename: str) -> None:
    with open(filename) as f:
        buffer = f.readlines()
    while True:
        stdscr.erase()
        for row, line in enumerate(buffer):
            stdscr.addstr(row, 0, line)

        k = stdscr.getkey()
        if k == "q":
            raise SystemExit(0)

def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    open_file(stdscr, args.filename)

    


if __name__ == "__main__":
    curses.wrapper(main)