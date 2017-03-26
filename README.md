# workspace.py
![](https://github.com/sqozz/workspace.py/raw/master/demo.gif)

An enhanced workspace generator for bars like yabar.
It is capable of pretty strong formatting on symbolds (i.e. FontAwesome ones) and can maybe adjusted to use images too. Urgent workspaces can change color or blink in a custom configurable pattern.

# Urgent workspaces
Workspaces that want to have attention, will cause workspace.py to dynamically format a symbol to produce a blinking label. The pattern of blinking can be configured by a format string, adjusted in speed or disabled completely.

# Polling
Polling in i3-py is broken atm. I've still no clue what exactly is going on but for yet there comes some magic string in the middle of a message from i3-IPC which i3-py cannot handle yet.
So for now workspace.py uses some adjustable loop which polls the current i3 workspace configuration.

# My usecase
I use this script with yabar to get some enhanced workspace overview. Configuration is pretty straigth forward since yabar calls this script once as continious procress piping out information for yabar to display.
