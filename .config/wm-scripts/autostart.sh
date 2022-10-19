#!/usr/bin/env bash

picom --experimental-backends &
dbus-launch --exit-with-session &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
pcmanfm -d &
nitrogen --restore &
dunst &
xsetroot -cursor_name left_ptr &
discord --start-minimized &

