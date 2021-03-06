# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from scripts import storage

import os
import subprocess
from libqtile import qtile
from libqtile import bar, layout, widget, hook
from libqtile.widget import base
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# default variables
mod = "mod4"
home_dir = os.path.expanduser("~")
terminal = "alacritty"
browser = "firefox"
vscode = "code"
fileManager = "Thunar"

keys = [
    # dmenu
    Key([mod], "p",
        lazy.spawn("dmenu_run -h 43 -i -p \"Run: \""),
        desc="Shows dmenu"
        ),

    # Programs
    Key([mod], "Return", lazy.spawn(terminal),
        desc=f"Open Terminal ({terminal})"),
    Key([mod], "b", lazy.spawn(browser),
        desc=f"Open Web Browser ({browser})"),
    Key([mod], "e", lazy.spawn(fileManager),
        desc=f"Open File Manager ({fileManager})"),
    Key([mod], "c", lazy.spawn(vscode),
        desc=f"Open Visual Studio Code ({vscode})"),

    # Change window state
    Key([mod], "f",          lazy.window.toggle_floating(),
        desc="Toggles window floating"),
    Key([mod, "shift"], "f",      lazy.window.toggle_fullscreen(),
        desc="Toggles window Full Screen"),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "i",          lazy.layout.grow(),
        desc="Grow focused Window"),
    Key([mod], "m",          lazy.layout.shrink(),
        desc="Shrink focused Window"),
    Key([mod, 'shift'], "i", lazy.layout.grow_main(),
        desc="Grow main Window"),
    Key([mod, 'shift'], "m", lazy.layout.shrink_main(),
        desc="Shrink main Window"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "control"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod],          "q", lazy.restart(),  desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

# custom workspace names and initialization
class Groupings:

    def init_group_names(self):
        return [("???", {"layout": "monadtall"}),     # Terminals
                ("???", {"layout": "monadtall"}),     # Web Browser
                ("???", {"layout": "monadtall"}),     # File Manager
                ("???", {"layout": "monadtall"}),     # Text Editor
                ("???", {"layout": "monadtall"}),     # Media
                ("???", {"layout": "monadtall"}),     # Gaming 
                ("???", {"layout": "monadtall"}),     # Virtualization
                ("???", {"layout": "monadtall"}),     # Messaging
                ("???", {"layout": "monadtall"})]    # Settings

    def init_groups(self):
        return [Group(name, **kwargs) for name, kwargs in group_names]


if __name__ in ["config", "__main__"]:
    group_names = Groupings().init_group_names()
    groups = Groupings().init_groups()

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 3,
                "margin": 8,
                "font": "Source Code Pro Medium",
                "font_size": 10,
                "border_focus": "#bd93f9",
                "border_normal": "#555555"
                }

# window layouts
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Stack(num_stacks=2, **layout_theme),
    layout.Bsp(**layout_theme),
    layout.Tile(**layout_theme),

    # Try more layouts by unleashing below layouts.
    # layout.Columns(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]


# nord for the bar/widgets/panel
def init_nord():
            # Polar night
    return [["#2e3440", "#2e3440"], # nord0
            ["#3b4252", "#3b4252"], # nord1
            ["#434c5e", "#434c5e"], # nord2
            ["#4c566a", "#4c566a"], # nord3
            # Snow Storm
            ["#d8dee9", "#d8dee9"], # nord4
            ["#e5e9f0", "#e5e9f0"], # nord5
            ["#eceff4", "#eceff4"], # nord6
            # Frost
            ["#8fbcbb", "#8fbcbb"], # nord7
            ["#88c0d0", "#88c0d0"], # nord8
            ["#81a1c1", "#81a1c1"], # nord9
            ["#5e81ac", "#5e81ac"], # nord10
            # Aurora
            ["#bf616a", "#bf616a"], # nord11
            ["#d08770", "#d08770"], # nord12
            ["#ebcb8b", "#ebcb8b"], # nord13
            ["#a3be8c", "#a3be8c"], # nord14
            ["#b48ead", "#b48ead"], # nord15
            ["#282a36", "#282a36"]] # background 

def nerd_icon(nerdfont_icon, fg_color):
    return widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                padding = 8,
                text = nerdfont_icon,
                foreground = fg_color,
                background = nord[16])


nord = init_nord()

widget_defaults = dict(
    font='Source Code Pro Medium',
    fontsize=12,
    padding=5,
)
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
            # Left Side of the bar

            widget.Spacer(
                length = 5,
                background = nord[16]
            ),
            widget.Image(
                filename = "~/.config/qtile/icons/python.png",
                background = nord[16],
                margin = 3,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(
                        terminal
                    ),
                    'Button3': lambda : qtile.cmd_spawn(
                        f'{terminal} -e nvim {home_dir}/.config/qtile/config.py'
                    )
                }
            ),
            widget.GroupBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                foreground = nord[15],
                background = nord[16],
                borderwidth = 4,
                disable_drag = True,
                highlight_method = "text",
                this_current_screen_border = nord[15],
                active = nord[10],
                inactive = nord[4],
                urgent_alert_method = 'line',
                urgent_border = nord[11]
            ),
            widget.Sep(
                size_percent = 60,
                margin = 5,
                linewidth = 2,
                background = nord[16],
                foreground = "#555555"
            ),
            widget.Spacer(
                length = bar.STRETCH,
                background = nord[16]
            ),

            # Center bar

            nerd_icon(
                "???",
                nord[11]
            ),
            widget.CurrentLayout(
                foreground = nord[4],
                background = nord[16]
            ),
            widget.Sep(
                size_percent = 60,
                margin = 5,
                linewidth = 2,
                background = nord[16],
                foreground = "#555555"
            ),
            nerd_icon(
                "???",
                nord[12]
            ),
            widget.CPU(
                format = "{load_percent}%",
                foreground = nord[4],
                background = nord[16],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e btop")
                }
            ),
            nerd_icon(
                "???",
                nord[13]
            ),
            widget.Memory(
                format = "{MemUsed:.0f}{mm}",
                foreground = nord[4],
                background = nord[16],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e btop")
                }
            ),
            nerd_icon(
                "???",
                nord[14]
            ),
            widget.GenPollText(
                foreground = nord[4],
                background = nord[16],
                update_interval = 5,
                func = lambda: storage.diskspace('FreeSpace'),
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e ncdu")
                }
            ),
            widget.Sep(
                size_percent = 60,
                margin = 5,
                linewidth = 2,
                background = nord[16],
                foreground = "#555555"
            ),
            nerd_icon(
                "???",
                nord[15]
            ),
            widget.GenPollText(
                foreground = nord[4],
                background = nord[16],
                update_interval = 5,
                func = lambda: subprocess.check_output(f"{home_dir}/.config/wm-scripts/num-installed-pkgs").decode("utf-8")
            ),

            # Left Side of the bar

            widget.Spacer(
                length = bar.STRETCH,
                background = nord[16]
            ),
            nerd_icon(
                "???",
                nord[8]
            ),
            widget.Net(
                format = "{down} ?????? {up}",
                foreground = nord[4],
                background = nord[16],
                update_interval = 2,
            ),
            widget.Sep(
                size_percent = 60,
                margin = 5,
                linewidth = 2,
                background = nord[16],
                foreground = "#555555"
            ),
            nerd_icon(
                "???",
                nord[9]
            ),
            widget.Clock(
                format = '%m/%d/%Y',
                foreground = nord[4],
                background = nord[16]
            ),
            nerd_icon(
                "???",
                nord[10]
            ),
            widget.Clock(
                format = '%I:%M %p',
                foreground = nord[4],
                background = nord[16]
            ),
            widget.Systray(
                background = nord[16]
            ),
            widget.Spacer(
                length = 5,
                background = nord[16]
            ),
        ]
    return widgets_list


# screens/bar
def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_list(), size=35, opacity=0.95, margin=[8, 8, 0, 8]))]

screens = init_screens()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

main = None
@hook.subscribe.startup_once
def start_once():
    start_script = os.path.expanduser("~/.config/wm-scripts/autostart.sh")
    subprocess.call([start_script])

@hook.subscribe.startup
def start_always():
    # fixes the cursor
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='Viewnior'),  # Photos/Viewnior 
    Match(wm_class='Alafloat'),  # Floating Alacritty Terminal 
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
