#!/usr/bin/env bash

picom --experimental-backends &
dbus-launch --exit-with-session &
nitrogen --restore &
dunst &
xsetroot -cursor_name left_ptr &
discord --start-minimized &
