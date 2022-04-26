#
## Imports                   
#

import os
import socket
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Match, Screen, Key, KeyChord, EzKey
from libqtile.lazy import lazy
from libqtile.utils import shuffle_down
from libqtile.log_utils import logger

#
## Variables
#

mod = 'mod4'
altMod = 'mod1'

MyTerminal = "kitty"
MyBrowser = "firefox"
MyEditor = "emacsclient -c -a 'emacs'"
MyEmacs = "emacsclient -c -a 'emacs'"
MyFileManager = "Thunar"

MyBorderFocus = '#686de0'
MyBorderNormal = '#281c34'
MyBorderWidth = 2
defMargin = 4
MyMargin = defMargin

EzKey.modifier_keys = {
    'M': mod,
    'A': altMod,
    'S': 'shift',
    'C': 'control',
}

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

#
## Functions
#


#
## Keybindings
#

keys = [
    # Base qtile
    Key([mod], "q",            lazy.restart(),                                 desc="Restarts Qtile"),
    Key([mod, 'shift'], "q",   lazy.shutdown(),                                desc="Close Qtile"),
    Key([mod, 'shift'], "c",   lazy.window.kill(),                             desc="Kills Focused Window"),

    # Run Menuhost
    Key([mod], "p", lazy.spawn("dmenu_run -h 24 -i -p \"Run: \""), desc="Shows dmenu"),
    #KeyChord([mod], "d",
    #    [
    #        Key([], "l", lazy.spawn("dm-logout"),   desc="Logout Dmenu"),
    #        Key([], "c", lazy.spawn("dm-colpick"),  desc="Colorpick Dmenu"),
    #        Key([], "d", lazy.spawn("dm-confedit"), desc="Config Dmenu"),
    #        Key([], "h", lazy.spawn("dm-hub"),      desc="Hub Dmenu"),
    #        Key([], "k", lazy.spawn("dm-kill"),     desc="Kill Dmenu"),
    #        Key([], "s", lazy.spawn("dm-maim"),     desc="Screenshot Dmenu"),
    #        Key([], "r", lazy.spawn("dm-record"),   desc="Record Dmenu"),
    #    ]
    #),
    #Key([mod], "p", lazy.spawn("rofi -show run"),            desc="Shows rofi"),

    # Useful Programs
    Key([mod], "Return",  lazy.spawn(MyTerminal),    desc="Open Terminal ({})".format(MyTerminal)),
    Key([mod], "b",       lazy.spawn(MyBrowser),     desc="Open Browser ({})".format(MyBrowser)),
    Key([mod], "e",       lazy.spawn(MyFileManager), desc="Open File Manager ({})".format(MyFileManager)),
    Key([mod], "c",       lazy.spawn('code'),        desc="Open Visual Studio Code"),
    Key(['control'], "e", lazy.spawn(MyEmacs),       desc="Start Emacs Client"),

    # Groups
    Key([mod], "comma",    lazy.screen.prev_group(), desc="Goes to previous group"),
    Key([mod], "period",   lazy.screen.next_group(), desc="Goes to next group"),

    # Change window state
    Key([mod], "f",          lazy.window.toggle_floating(),   desc="Toggles window floating"),
    Key([mod], "space",      lazy.window.toggle_fullscreen(), desc="Toggles window Full Screen"),

    # Layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Changes Layouts"),

    # Window Navigation
    Key([mod], "j",          lazy.layout.down(),         desc="Move focus to the up window"),
    Key([mod], "k",          lazy.layout.up(),           desc="Move focus to the down window"),
    Key([mod, 'shift'], "j", lazy.layout.shuffle_down(), desc="Suffle down on the Windows"),
    Key([mod, 'shift'], "k", lazy.layout.shuffle_up(),   desc="Suffle up on the Windows"),

    # Window Resizing
    Key([mod], "i",          lazy.layout.grow(),        desc="Grow focused Window"),
    Key([mod], "m",          lazy.layout.shrink(),      desc="Shrink focused Window"),
    Key([mod, 'shift'], "i", lazy.layout.grow_main(),   desc="Grow main Window"),
    Key([mod, 'shift'], "m", lazy.layout.shrink_main(), desc="Shrink main Window"),
    Key([mod], "n",          lazy.layout.reset(),       desc="Restore secondary Windows to its default ratio"),
     
    ]

#
## Groups
#

group_names = 'dev www sys doc vbox chat mus vid gfx'.split()
groups = [Group(name, layout='monadtall') for name in group_names]

for i, name in enumerate(group_names):
    indx = str(i + 1)
    keys += [
        # mod1 + letter of group = switch to group
        EzKey("M-{}".format(indx), lazy.group[name].toscreen(),
            desc="Switch to group {}".format(name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        EzKey("M-S-{}".format(indx), lazy.window.togroup(name), lazy.group[name].toscreen(),
            desc="Switch to & move focused window to group {}".format(name)),
    ]

#
## Layouts
#

layouts_theme = {
    "border_focus": MyBorderFocus,
    "border_normal": MyBorderNormal,
    "border_width": MyBorderWidth,
    "margin": MyMargin,
}

layouts = [
    layout.MonadTall(**layouts_theme),
    layout.Max(**layouts_theme),
    layout.Floating(**layouts_theme),
]

#
## Widgets / Extentions
#

colors = [["#2e3440", "#2e3440"], # panel background
          ["#434c5e", "#4c566a"], # background for current screen tab
          ["#eceff4", "#eceff4"], # font color for group names
          ["#5e81ac", "#5e81ac"], # border line color for current tab
          ["#81a1c1", "#81a1c1"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#5e81ac", "#5e81ac"], # color for the 'even widgets'
          ["#81a1c1", "#81a1c1"], # window name
          ["#88c0d0", "#88c0d0"]] # backbround for inactive screens

widget_defaults = dict(
    font="UbuntuMono NF",
    fontsize = 12,
    padding = 3,
    background=colors[2]
)

extension_defaults = widget_defaults.copy()

#
## Widget Customization
#

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Image(
                       filename = "~/.config/qtile/icons/python.png",
                       scale = "False",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(MyTerminal)},
                       background = colors[0]
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 11,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[7],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = colors[3],
                       background = colors[1]
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 40,
                       foreground = colors[2],
                       background = colors[0]
                       ),
             #widget.WindowName(
             #         foreground = colors[6],
             #         background = colors[0],
             #         padding = 0
             #         ),
              widget.TaskList(
                      #foreground = colors[6],
                       background = colors[0],
                       rounded = False,
                       txt_floating = '🗗 ',
                       txt_maximized = '🗖 ',
                       txt_minimized = '🗕 '
                       ),
              widget.Systray(
                       background = colors[0],
                       padding = 5
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.TextBox(
                       text = '',
                       font = 'FiraCode NF',
                       foreground = '#bf616a',
                       background = colors[0],
                       padding = -4.1,
                       fontsize = 37
                       ),
              widget.TextBox(
                       text = '🗇',
                       padding = 2,
                       foreground = colors[2],
                       background = '#bf616a',
                       fontsize = 11
                       ),
              widget.WindowCount(
                       foreground = colors[2],
                       background = '#bf616a',
                       padding = 5,
                       show_zero = True,
                       ),
              widget.TextBox(
                       text = '',
                       font = 'FiraCode NF',
                       foreground = '#d08770',
                       background = '#bf616a',
                       padding = -4.1,
                       fontsize = 37
                       ),
              widget.TextBox(
                       text = " 🖬",
                       foreground = colors[2],
                       background = '#d08770',
                       padding = 0,
                       fontsize = 14
                       ),
              widget.Memory(
                       foreground = colors[2],
                       background = '#d08770',
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(MyTerminal + ' -e btop')},
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       font = 'FiraCode NF',
                       foreground = '#ebcb8b',
                       background = '#d08770',
                       padding = -4.1,
                       fontsize = 37
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[2],
                       background = '#ebcb8b',
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = '#ebcb8b',
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       font = 'FiraCode NF',
                       foreground = '#a3be8c',
                       background = '#ebcb8b',
                       padding = -4.1,
                       fontsize = 37
                       ),
              widget.Clock(
                       foreground = colors[2],
                       background = '#a3be8c',
                       format = "%d/%m - %H:%M"
                       ),
              widget.TextBox(
                       text = '',
                       font = 'FiraCode NF',
                       foreground = '#b48ead',
                       background = '#a3be8c',
                       padding = -4.1,
                       fontsize = 37
                       ),
              widget.QuickExit(
                       default_text = '⏻  Exit',
                       countdown_format = '⏻  {}sec',
                       foreground = colors[2],
                       background = '#b48ead',
                       padding = 5
                       ),
              ]

#
## Screens
#

screens = [
    Screen(
        top=bar.Bar(widgets_list, 24, margin=0),
    ),
]

#
## Mouse for Floating Layouts
# 

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
],
    border_focus=MyBorderFocus,
    border_normal=MyBorderNormal,
    border_width=1,
)

#
## Auto Startup
#

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

wmname = "LG3D"
