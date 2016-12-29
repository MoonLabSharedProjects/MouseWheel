import time
import curses
import sys

stdscr = curses.initscr()

def loop():
    numbers = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0,1, 2, 3, 2, 1, 0,1, 2, 3, 2, 1, 0,1, 2, 3, 2, 1, 0,1, 2, 3, 2, 1, 0,]
    list = ["Initiating    ", "Initiating.   ", "Initiating..  ", "Initiating... ", ]
    counter = 0
    for i in range(len(numbers)):
        stdscr.addstr(7, 4, list[numbers[counter]])
        time.sleep(0.5)
        counter += 1
        stdscr.refresh()
loop()