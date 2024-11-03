# frufw
### A simple firewall with a terminal UI ```(written in python)```, while being easy to use.
### Supports  most comonly used init systems, that use iptables.
> [!CAUTION]
> This program is in It's very early stages and mostly is a concept rather than a necessity, priority or superiority towards other programs

> [!WARNING]
> This tool is only and intented, for linux based OS'es

### Requiremnets:
```
pip install curses subprocess argparse
```

> [!TIP]
> Make sure to update the packages before hand with ``` python -m pip install --upgrade pip ```

# 🚀 Usage Instructions
## Run the program by using ``` python``` (or python3) ``` frufw.py```
### You will be prompted with the following:
```
Please specify an option:
 -tui to run the Terminal UI
 -v for version
 -h for help.
```
## The ```-tui``` command ``` (Terminal UI) ```,
will display a managment control panel for blocking or allowing ip adresses through ``` iptables ```, and is easy to use through
> the arrow keys, such as up/down, and the use of enter for selecting the option.
> To input an ip to block simply use the keyboard characters and hit enter to add that rule, the rule will be displayed in your list/iptables file configuration.
## The usage screen mostly consits of a panel where the user is able to view their firewall rules or change them easily

> [!NOTE]
> If you happen to encounter some errors ,please make sure to read the logs, and issue a report in this repo.

## Output of ```-tui``` usage
> (Terminal UI command)

![oie_iBZz85O5y2wF](https://github.com/user-attachments/assets/0d5cf65b-0669-45fc-8d8c-4bd2dbaf816d)
## The ```-v``` command will show the verison,
``` Version 1.0.0 (or later) ```
## The ```-h``` will print a help screen with the following:
```

Usage: frufw.py [options]
Options:

  -h, --help      Show this help message and exit

  -v, --version   Show version information and exit

  -tui            Run the TUI interface
```
> This info is useful if you have not read the ```README```

## End of ```README.Md``` or ```Usage instructions```
> [!NOTE]
> Use and modification of this code is allowed```(under the following of the GNU V3.0 License. Such as no close sourcing of this software, or harmed/misintepreted use.)``` and encouraged.
