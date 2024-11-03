import curses
import subprocess
import argparse
import sys

splash_text = """
.########.########..##.....##.########.##......##
.##.......##.....##.##.....##.##.......##..##..##
.##.......##.....##.##.....##.##.......##..##..##
.######...########..##.....##.######...##..##..##
.##.......##...##...##.....##.##.......##..##..##
.##.......##....##..##.....##.##.......##..##..##
.##.......##.....##..#######..##........###..###.
                           - by florwithmriver0
===================================
Welcome to Firewall Management Tool
===================================
"""

VERSION = "1.0.0"

def start_firewall():
    print("Starting the firewall... ")

def stop_firewall():
    print("Stopping the firewall... ")

def add_rule(ip):
    try:
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], check=True)
        return f"Added rule to drop traffic from IP: {ip}"
    except subprocess.CalledProcessError:
        return f"Failed to add rule for IP: {ip}"

def remove_rule(ip):
    try:
        subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'], check=True)
        return f"Removed rule for IP: {ip}"
    except subprocess.CalledProcessError:
        return f"Failed to remove rule for IP: {ip}"

def show_rules(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Current Firewall Rules:", curses.A_BOLD)

    try:
        result = subprocess.run(['sudo', 'iptables', '-L', '-n'], stdout=subprocess.PIPE, text=True, check=True)
        rules = result.stdout.splitlines()
        max_lines = curses.LINES - 2
        offset = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Current Firewall Rules:", curses.A_BOLD)
            for idx, rule in enumerate(rules[offset:offset + max_lines]):
                stdscr.addstr(idx + 1, 0, rule)

            if offset + max_lines < len(rules):
                stdscr.addstr(max_lines + 1, 0, "Press Enter to see more, or 'b' to go back...")
            else:
                stdscr.addstr(max_lines + 1, 0, "Press 'b' to go back...")

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_ENTER or key in [10, 13]:
                offset += max_lines
                if offset >= len(rules):
                    offset = len(rules) - max_lines  # Prevent going beyond available rules
            elif key == ord('b'):
                break

    except subprocess.CalledProcessError:
        stdscr.addstr(1, 0, "Failed to retrieve rules.")
        stdscr.addstr(2, 0, "Press any key to go back...")
        stdscr.refresh()
        stdscr.getch()

def show_logs(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Firewall Logs:", curses.A_BOLD)

    try:
        result = subprocess.run(['sudo', 'journalctl', '-u', 'iptables'], stdout=subprocess.PIPE, text=True, check=True)
        logs = result.stdout.splitlines()
        max_lines = curses.LINES - 2
        
        for idx, log in enumerate(logs[:max_lines]):
            stdscr.addstr(idx + 1, 0, log)

        if len(logs) > max_lines:
            stdscr.addstr(max_lines + 1, 0, "Press any key to go back...")
        else:
            stdscr.addstr(len(logs) + 1, 0, "Press any key to go back...")
    except subprocess.CalledProcessError:
        stdscr.addstr(1, 0, "Failed to retrieve logs.")
    
    stdscr.refresh()
    stdscr.getch()

def print_splash_screen(stdscr, theme):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    
    for idx, line in enumerate(splash_text.strip().splitlines()):
        centered_x = (max_x - len(line)) // 2
        stdscr.addstr(idx, centered_x, line, curses.color_pair(1) if theme == 'dark' else curses.color_pair(2))

def center_text(text, stdscr, row, theme):
    max_y, max_x = stdscr.getmaxyx()
    centered_x = (max_x - len(text)) // 2
    stdscr.addstr(row, centered_x, text, curses.color_pair(1) if theme == 'dark' else curses.color_pair(2))

def print_menu(stdscr, highlight, theme):
    stdscr.clear()
    print_splash_screen(stdscr, theme)
    center_text("Firewall Management Menu", stdscr, len(splash_text.strip().splitlines()) + 2, theme)

    menu_items = [
        "Start Firewall",
        "Stop Firewall",
        "Add Rule",
        "Remove Rule",
        "Show Rules",
        "Show Logs",
        "Theme: Dark/Light",
        "Exit"
    ]
    
    for idx, item in enumerate(menu_items):
        if idx == highlight:
            stdscr.addstr(idx + len(splash_text.strip().splitlines()) + 4, (curses.COLS - len(item)) // 2, item, curses.color_pair(3))
        else:
            stdscr.addstr(idx + len(splash_text.strip().splitlines()) + 4, (curses.COLS - len(item)) // 2, item, curses.color_pair(1) if theme == 'dark' else curses.color_pair(2))

    stdscr.refresh()

def handle_input(stdscr):
    highlight = 0
    theme = 'dark'  # Default theme
    while True:
        print_menu(stdscr, highlight, theme)
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            highlight = (highlight - 1) % 8
        elif key == curses.KEY_DOWN:
            highlight = (highlight + 1) % 8
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if highlight == 0:
                start_firewall()
            elif highlight == 1:
                stop_firewall()
            elif highlight == 2:
                stdscr.clear()
                stdscr.addstr(0, 0, "Enter IP to add: ")
                curses.echo()
                ip = stdscr.getstr().decode('utf-8')
                curses.noecho()
                result_message = add_rule(ip)
                stdscr.addstr(2, 0, result_message)
                stdscr.addstr(3, 0, "Press any key to go back...")
                stdscr.refresh()
                stdscr.getch()
            elif highlight == 3:
                stdscr.clear()
                stdscr.addstr(0, 0, "Enter IP to remove: ")
                curses.echo()
                ip = stdscr.getstr().decode('utf-8')
                curses.noecho()
                result_message = remove_rule(ip)
                stdscr.addstr(2, 0, result_message)
                stdscr.addstr(3, 0, "Press any key to go back...")
                stdscr.refresh()
                stdscr.getch()
            elif highlight == 4:
                show_rules(stdscr)
            elif highlight == 5:
                show_logs(stdscr)
            elif highlight == 6:
                # Toggle theme
                theme = 'light' if theme == 'dark' else 'dark'
            elif highlight == 7:
                break

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Dark theme
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Light theme
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight color

    curses.curs_set(0)
    handle_input(stdscr)

def print_version():
    print(f"Firewall Management Tool Version: {VERSION}")

def print_help():
    help_text = """
Usage: firewall_tui.py [options]
Options:
  -h, --help      Show this help message and exit
  -v, --version   Show version information and exit
  -tui            Run the TUI interface
"""
    print(help_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-v', '--version', action='store_true', help='Show version information')
    parser.add_argument('-h', '--help', action='store_true', help='Show help message')
    parser.add_argument('-tui', action='store_true', help='Run the TUI interface')

    args = parser.parse_args()

    if args.version:
        print_version()
        sys.exit(0)

    if args.help:
        print_help()
        sys.exit(0)

    if args.tui:
        curses.wrapper(main)
    else:
        print("Please specify an option: \n -tui to run the Terminal UI\n -v for version\n -h for help.")

